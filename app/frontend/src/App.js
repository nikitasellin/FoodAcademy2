import React from 'react';
import { 
  BrowserRouter as Router, 
  Route,
 } from  'react-router-dom';
import { connect } from 'react-redux';
import Navbar from './components/Navbar';
import CoursesList from './components/courses/CoursesList';
import CourseDetails from './components/courses/CourseDetails';
import CourseSubscription from './components/courses/CourseSubscription';
import Login from './components/users/Login';
import Logout from './components/users/Logout';
import { autoLogin } from './redux/actions';
import './App.css';


const BaseLayout = () => (
  <div>
    <Navbar />
    <div className="content">
      <Route path="/courses/details/:pk/" component={CourseDetails} />
      <Route path="/courses/subscription/:pk/" component={CourseSubscription} />
      <Route path="/login/" component={Login} />
      <Route path="/logout/" component={Logout} />
      <Route path="/" exact component={CoursesList} />
    </div>
  </div>
)

class App extends React.Component {
  componentDidMount(){
    this.props.autoLogin()
  }

  render () {
    return(
      <Router>
        <BaseLayout />
      </Router>
    );
  }
}

const mapStateToProps = (state) => {
  return {
    userReducer: state.userReducer
  }
}

const mapDispatchToProps = (dispatch) => {
  return {
    autoLogin: () => dispatch(autoLogin())
  }
}

export default connect(mapStateToProps, mapDispatchToProps)(App);
