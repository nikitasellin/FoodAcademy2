import React from 'react';
import { Redirect } from 'react-router-dom';
import { connect } from 'react-redux';
import { logOut } from '../../redux/actions';


class Logout extends React.Component {
  componentDidMount() {
    this.props.dispatch(logOut());
  }

  render() {
    return (
      <Redirect to="/login/" />
    );
  }
}


export default connect()(Logout);
