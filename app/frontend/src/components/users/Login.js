import React from 'react';
import { connect } from 'react-redux';
import { fetchUser } from '../../redux/actions';


// @TODO! Create "Personal Area" component and do redirect after login.
class Login extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      email: '',
      password: '',
    };
    this.handleChange  =  this.handleChange.bind(this);
    this.handleSubmit  =  this.handleSubmit.bind(this);
    document.title = 'Авторизация';
  }

  handleChange = (event) => {
    this.setState({
      [event.target.name]: event.target.value
    });
  }

  handleSubmit = (event) => {
    event.preventDefault();
    this.props.fetchUser(this.state);
  }

  // @TODO! Handle form errors.
  render() {
    return (
      <form onSubmit={this.handleSubmit}>
        <div className="container col-md-3">
          <h1 className="text-center">Страница авторизации</h1>
          <div className="form-group">
            <div className="row">
              <div className="col-lg-4 text-right">
                <label>E-mail:</label>
              </div>
              <div className="col-lg-8 text-left">
                <input
                  name='email'
                  placeholder='Введите e-mail'
                  value={this.state.email}
                  onChange={this.handleChange}
                />
              </div>
            </div>
          </div>
          <div className="form-group">
            <div className="row">
              <div className="col-lg-4 text-right">
                <label>Пароль:</label>
              </div>
              <div className="col-lg-8 text-left">
                <input
                  type='password'
                  name='password'
                  placeholder='Введите пароль'
                  value={this.state.password}
                  onChange={this.handleChange}
                />
              </div>
            </div>
          </div>
          <div className="form-group">
            <div className="row">
              <div className="col-lg-4 text-right">
              </div>
              <div className="col-lg-8 text-left">
                <input type='submit' value="Ввод" />
              </div>
            </div>
          </div>
        </div>
      </form>
    )
  }
}

const mapDispatchToProps = (dispatch) => {
  return {
      fetchUser: (userInfo) => dispatch(fetchUser(userInfo))
  }
}

export default connect(null, mapDispatchToProps)(Login);
