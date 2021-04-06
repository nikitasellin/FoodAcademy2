import { combineReducers } from 'redux'


const initialState = {
  loggedIn: false,
  user: {}
}

const userReducer = (state = initialState, action) => {
  switch(action.type){
    case "LOG_IN":
      console.log('Logging in...');
      return {
        loggedIn: true,
        user: {...action.payload}
      }
    case "LOG_OUT":
      console.log('Logging out...');
      localStorage.clear();
      return {
        loggedIn: false,
        user: {}
      }
    default: return state
  }
}

const rootReducer = combineReducers({
    userReducer,
})

export default rootReducer;
