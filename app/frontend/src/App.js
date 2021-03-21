// import logo from './logo.svg';
// import './App.css';
import React from 'react';
import CoursesList from './components/courses';


const BaseLayout = () => (
  <div>
    <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
      <button className="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav">
        <span className="navbar-toggler-icon"></span>
      </button>
      <a className="navbar-brand" href="#">FoodAcademy</a>
      <div className="navbar-collapse collapse justify-content-center" id="navbarNav">
        <ul className="navbar-nav text-center">
          <li className="nav-item">
            <a className="nav-link" href="/">Курсы</a>
          </li>
          <li className="nav-item">
            <a className="nav-link" href="#">Преподаватели</a>
          </li>
          <li className="nav-item">
            <a className="nav-link" href="#">Контакты</a>
          </li>
        </ul>
      </div>
    </nav>

    <div className="content">
      <CoursesList url='http://127.0.0.1:8000/api/view/courses/' />
    </div>
  </div>
)


class App extends React.Component {
  render () {
    return(
      <BaseLayout />
    );
  }
}

export default App;
