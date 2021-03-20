import axios from "axios"

// Render courses list via fetch
const coursesListUrl = 'http://127.0.0.1:8000/api/view/courses/';


function getCoursesList() {
    let coursesContainer = document.querySelector("#coursesList");
    coursesContainer.innerHTML = '';
    
    fetch(coursesListUrl)
        .then((response)=> response.json())
            .then(function (data) {
                coursesContainer.innerHTML = generateCoursesHtmlOutput(data);
        })
        .catch(function (error) {
            console.log(error);
        });   
}


function generateCoursesHtmlOutput(data) {
    if (!data) {
        console.log('Unknown error!');
        return '<h1>Список курсов пуст!</h1>'
    }
    let result = '<table class="table table-bordered table-responsive"><thead><th>Название курса</th><th>Описание курса</th></thead><tdoby>';
    coursesList = data.results; 
    for (const i in coursesList) {
        result += '<tr><td>' + coursesList[i].title + '</td>';
        result += '<td>' + coursesList[i].description + '</td></tr>';
    }
    result += '</tbody></table>';
    return result;
}


let fetchButton = document.querySelector('#fetchButton');
if (fetchButton) {
    fetchButton.addEventListener('click', getCoursesList);
}


// Render teachers list via axios
const teachersListUrl = 'http://127.0.0.1:8000/api/view/teachers/';


function getTeachersList() {
    let teachersContainer = document.querySelector("#teachersList");
    teachersContainer.innerHTML = ''; 

    axios.get(teachersListUrl)
        .then(function (response) {
            teachersContainer.innerHTML = generateTeachersHtmlOutput(response);
        })
        .catch(function (error) {
            console.log(error);
        });   
}


function generateTeachersHtmlOutput(response) {
    if (response.status !== 200) {
        console.log('Unknown error! Response status is: ' + response.status);
        return '<h1>Не удалось загрузить список преподавателей!</h1>'
    }
    let result = '<table class="table table-bordered table-responsive"><thead><th>Имя</th><th>Фамилия</th></thead><tdoby>';
    let teachersList = response.data.results;
    for (const i in teachersList) {
        result += '<tr><td>' + teachersList[i].first_name + '</td>';
        result += '<td>' + teachersList[i].last_name + '</td></tr>';
    }
    result += '</tbody></table>';
    return result;
}


let axiosButton = document.querySelector('#axiosButton');
if (axiosButton) {
    axiosButton.addEventListener('click', getTeachersList)    
}


// Get and refresh token
const obtainTokenUrl = 'http://127.0.0.1:8000/api/token/';
const refreshTokenUrl = 'http://127.0.0.1:8000/api/token/refresh/';


function parseFormData(data) {
    if (data.refreshToken) {
        return { 
            url: refreshTokenUrl,
            postData: {
                refresh: data.refreshToken,
            }
        }
    };
    return {
        url: obtainTokenUrl,
        postData: {
            email: data.email,
            password: data.password
        }
    };
};


function renderTokens(access, refresh) {
    const atContainer = document.querySelector('#accessToken');
    const rtContainer = document.querySelector('#refreshToken');
    atContainer.innerHTML = '<b>' + access + '</b>';
    rtContainer.innerHTML = '<b>' + refresh + '</b>';
}


$(document).ready(function () {
    $("#tokenForm").submit(function(e) {
        e.preventDefault(); // Avoid to execute the actual submit of the form

        const form = $(this);
        const formData = form.serializeArray().reduce(function(obj, item) {
            obj[item.name] = item.value;
            return obj;
        }, {});

        const params = parseFormData(formData);
        $.ajax({
            type: 'POST',
            url: params.url,
            data: params.postData,
            success: function(data)
            {   
                let accessToken = data.access;
                let refreshToken = data.refresh;
                if (params.postData.refresh) {
                    refreshToken = params.postData.refresh;
                };
                renderTokens(accessToken, refreshToken);
            },
            error: function (xhr, status, exception) {
                console.log(xhr, status, exception);
                alert('Ошибка при получении данных: ' + exception);
            }
        });
    });
});
