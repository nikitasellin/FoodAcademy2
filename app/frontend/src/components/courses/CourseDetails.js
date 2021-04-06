import React from 'react';
import { Link } from 'react-router-dom';
import { connect } from 'react-redux';
import Loader from "react-loader-spinner";
import CoursesService from './CoursesService';

const coursesService = new CoursesService();

const TeachersBlock = ({courseTeachers}) =>
{   
  if (courseTeachers){
    return (
      <div>
        <b>Курс ведут преподаватели:</b>
        <hr />
        {courseTeachers.map((teacher) => 
          <div key={teacher.id}>
            {/* @TODO! Replace it with Link */}
            <a href={"/teachers/details/" + teacher.id + "/"}>{teacher.first_name} {teacher.last_name}</a>
          </div>)
        }
        <hr/>
      </div>
    );
  }
  return null;
}

const SubscriptionBlock = (props) =>
{ 
  const {isLoggedIn, userRole, courseID} = props;
  if (!isLoggedIn) {
    return(
      <div>
        Для записи на курс необходимо <Link to={"/login/"}>авторизоваться</Link> с учётной записью студента
        <hr />
      </div>
    );
  }
  if (userRole === 'student') {
    return(
      <div>
       <Link to={"/courses/subscription/" + courseID + "/"}>Записаться</Link> на курс
       <hr/>
      </div>
    );
  }
  return null;
}

class CourseDetails extends React.Component {
  constructor(props) {
    super(props);
    const { match: { params } } = this.props;
    let pk = null;
    if(params && params.pk) {
      pk = params.pk
    };
    this.state = {
      courseDetails: '',
      courseID: pk,
    }
    document.title = 'Подробная информация о курсе';
  }

  componentDidMount() {
    // @TODO! Redirect on error.
    if (this.state.courseID) {
      let self = this;
      coursesService.getCourse(this.state.courseID)
        .then((data) => {
          self.setState({ 
            courseDetails: data,
            })
          })
        .catch((error) => {
          console.log(error);
      });
    }
  }

  render() {
    return(
      <div className="container col-lg-6">
        <h1 className="text-center">Описание курса</h1>
        <hr />
        {
          !this.state.courseDetails
          ?
            <div className="container text-center">
              <Loader
                type="Grid"
                color="grey"
                height={200}
                width={200}
                timeout={5000}
              /> 
            </div>
          :
            <div className="row">
              <div className="col-lg-4 text-left">
                <img src={this.state.courseDetails.image} className="img-thumbnail" alt="Изображение" />
              </div>
              <div className="col-lg-8 text-left">
                <b>{this.state.courseDetails.title}</b>
                <hr />
                {this.state.courseDetails.description}
                <hr />
                <TeachersBlock 
                  courseTeachers={this.state.courseDetails.teachers} 
                />
                <SubscriptionBlock 
                  isLoggedIn={this.props.userReducer.loggedIn} 
                  userRole={this.props.userReducer.user.role}
                  courseID={this.state.courseID}
                />
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

export default connect(mapStateToProps, null)(CourseDetails);
