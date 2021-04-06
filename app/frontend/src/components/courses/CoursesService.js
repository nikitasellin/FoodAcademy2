import { handleFetchErrors } from '../../utils';


// @TODO! Change with real URL in production, or use environment variables.
const API_URL = 'http://localhost:8000/api';

class CoursesService {
    getCoursesList() {
        const url = `${API_URL}/view/courses/`;
        return fetch(url)
        .then(response => handleFetchErrors(response))
    }
    getCoursesListByURL(link){
        const url = link;
        return fetch(url)
        .then(response => handleFetchErrors(response))
    }
    getCourse(pk) {
        const url = `${API_URL}/view/courses/${pk}/`;
        return fetch(url)
        .then(response => handleFetchErrors(response))
    }
    subscribeToCourse(props) {
        const url = `${API_URL}/full-access/groups/${props.courseGroupID}/`;
        return fetch(url, {
            method: "PATCH",
            headers: {
              "Content-Type": "application/json",
              "Accept": "application/json",
              "Authorization": `Bearer ${props.authToken}`
            },
            body: JSON.stringify({newStudent: props.studentID})
        })
        .then(response => handleFetchErrors(response))
    }
}

export default CoursesService;
