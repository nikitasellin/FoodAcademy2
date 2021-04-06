import React from 'react';
import { NavLink } from 'react-router-dom';
import { connect } from 'react-redux';


// @TODO! Add 'Admin block' (create Course and Teacher).
class Navbar extends React.Component {
  render () {
    return (
      <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
        <button className="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav">
          <span className="navbar-toggler-icon"></span>
        </button>
        <a className="navbar-brand" href="#">FoodAcademy</a>
        <div className="navbar-collapse collapse justify-content-center" id="navbarNav">
          <ul className="navbar-nav text-center">
            <li className="nav-item">
              <NavLink to="/" activeClassName="nav-link">
                Курсы
              </NavLink>
            </li>
            <li className="nav-item">
            <NavLink to="#" activeClassName="nav-link">
                Преподаватели
              </NavLink>
            </li>
            <li className="nav-item">
              <NavLink to="#" activeClassName="nav-link">
                Контакты
              </NavLink>
            </li>
          </ul>
        </div>
        <div className="dropdown">
          <button className="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
            { !this.props.userReducer.loggedIn 
              ? <span>Вход/Регистрация</span>
              : <span>Здравствуйте, {this.props.userReducer.user.full_name}</span>
            }
          </button>
          { 
            !this.props.userReducer.loggedIn 
              ? 
                <div className="dropdown-menu" aria-labelledby="dropdownMenuButton">
                  <NavLink to="/login/" className="dropdown-item" activeClassName="">
                    Вход
                  </NavLink>
                  <div className="dropdown-divider"></div>
                  <NavLink to="/signup/" className="dropdown-item" activeClassName="">
                    Регистрация
                  </NavLink>
                </div>
              : 
                <div className="dropdown-menu" aria-labelledby="dropdownMenuButton">
                  <NavLink to="#" className="dropdown-item" activeClassName="">
                    Личный кабинет
                  </NavLink>
                  <div className="dropdown-divider"></div>
                  <NavLink to="/logout/" className="dropdown-item" activeClassName="">
                    Выход
                  </NavLink>
                </div>
           }
        </div>
      </nav>
    );
  }
}

const mapStateToProps = (state) => {
  return {
    userReducer: state.userReducer
  }
}

export default connect(mapStateToProps, null)(Navbar);
