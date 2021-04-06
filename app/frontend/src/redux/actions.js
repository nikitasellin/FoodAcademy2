import { handleFetchErrors } from '../utils';


// @TODO! Change with real URL in production, or use environment variables.
const API_URL = 'http://localhost:8000/api';

const logIn = (payload) => ({ type: "LOG_IN", payload})

export const logOut = () => ({type: "LOG_OUT"})

export const fetchUser = (userInfo) => dispatch => {
    fetch(`${API_URL}/token/obtain/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Accept": "application/json"
      },
      body: JSON.stringify(userInfo)
    })
    .then(response => handleFetchErrors(response))
    .then(data => {
      localStorage.setItem("access", data.access);
      localStorage.setItem("refresh", data.refresh);
      dispatch(logIn(data.user));
    })
    .catch(error => console.log(error));
}

export const autoLogin = () => dispatch => {
    fetch(`${API_URL}/token/refresh/`, {
      method: "POST",  
      headers: {
          "Content-Type": "application/json",
          "Accept": "application/json",
        },
        body: JSON.stringify(
          {
            "refresh": localStorage.getItem("refresh")
          })
      })
    .then(response => handleFetchErrors(response))
    .then(data => {
        localStorage.setItem("access", data.access);
        dispatch(logIn(data.user));
    })
  .catch(error => console.log(error));
}
