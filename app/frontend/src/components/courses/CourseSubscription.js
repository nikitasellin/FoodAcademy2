import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { connect } from 'react-redux';
import CoursesService from './CoursesService';


const coursesService = new CoursesService();

const SelectGroupBlock = (props) => {
  const {studentID, formOptions} = props;
  const [isSubscribed, setIsSubscribed] = useState(false);

  // @TODO! Check token before sending form data.
  const handleSubmit = (event) => {
    event.preventDefault();
    const groupID = event.target[0].value;
    coursesService.subscribeToCourse(
      {
        courseGroupID: groupID,
        studentID: studentID,
        authToken: localStorage.getItem('access')  
      })
      .then(data => {
        alert('Ваша группа: ' + data.title);
        setIsSubscribed(true);
      })
      .catch(error => alert('Ошибка! ' + error));
  }
  
  return(
    isSubscribed
    ? <h5 className="alert-success">Вы успешно записались на курс!</h5>
    :
      <form onSubmit={handleSubmit}>
        <select>
          {
            formOptions.map(
              option => (option)
            )
          }
        </select>
        <input type="submit" className="btn btn-sm btn-dark" value="Записаться" />
      </form>
  );
}

const SubscriptionBlock = (props) => {
  const { studentID, courseGroups } = props;
  const [alertMessage, setAlertMessage] = useState('');
  
  const makeFormOptions = (courseGroups) => {
    let tmpOptions = [];
    if (courseGroups) {
      courseGroups.forEach(
        (group) => {
          tmpOptions.push(
            <option 
              key={group.id} 
              value={group.id}
            >
              {group.title} (c {group.start_date})
            </option>)
        }
      )
    }
    return tmpOptions
  }

  useEffect(() => {
    if (!courseGroups) {
      setAlertMessage('');
    } else {
      courseGroups.length > 0
      ? 
        courseGroups.forEach(
          (group) => {
            if (group.students.includes(studentID)) {
              setAlertMessage('Вы уже обучаетесь на этом курсе!');
            }
          }
        )
      : setAlertMessage('Нет доступных групп для записи!');
    }
  }, [alertMessage, studentID, courseGroups]);

  return(
    alertMessage
    ? <h5 className="alert-warning">{alertMessage}</h5>
    :
      <SelectGroupBlock
        studentID={studentID}
        formOptions={makeFormOptions(courseGroups)}
      />
  );
}

class CourseSubscription extends React.Component {
  constructor(props) {
    super(props);
    const { match: { params } } = this.props;
    let pk = null;
    if(params && params.pk) {
      pk = params.pk
    };
    this.state = {
      courseTitle: '',
      courseGroups: null,
      courseID: pk,
      alreadyOnCourse: false
    }
    document.title = 'Запись на курс';
  }

  // @TODO! Handle errors.
  componentDidMount() {
    if (this.state.courseID) {
      let self = this;
      coursesService.getCourse(this.state.courseID)
        .then(function (data) {
          self.setState({ 
            courseTitle: data.title,
            courseGroups: data.course_group,
            })
          })
        .catch(function (error) {
          console.log(error);
      });
    }
  }

  render() {
    return(
      <div className="container col-lg-6">
        <h1 className="text-center">Запись на курс "{this.state.courseTitle}" </h1>
        <hr />
        { !this.props.userReducer.loggedIn || this.props.userReducer.user.role !== 'student'
          ? <p className="text-center">Для записи на курс необходимо <Link to={"/login/"}>авторизоваться</Link> с учётной записью студента</p>
          : <div className="row">
              <div className="col-lg-4 text-right">
                Выберите группу:
              </div>
              <div className="col-lg-8 text-left">
               <SubscriptionBlock 
                studentID={this.props.userReducer.user.pk}
                courseGroups={this.state.courseGroups} />
              </div>
            </div>
        }        
      </div>
    );
  }
}

const mapStateToProps = (state) => {
  return {
    userReducer: state.userReducer
  }
}

export default connect(mapStateToProps, null)(CourseSubscription);
