import rootReducer from './reducers';

it('return the initial state', () => {
  expect(rootReducer(undefined, {})).toEqual({
    'userReducer': {
      loggedIn: false,
      user: {}
    }
  });
});


it('log in action', () => {
  const previousState = {
    'userReducer': {
      loggedIn: false,
      user: {}
    }
  };
  const fakeUser = {
    "pk": 1,
    "full_name": "Nikita Selin",
    "email": "nikita@selin.com.ru",
    "role": "administrator"
  };
  const logInAction = {
    'type': 'LOG_IN',
    'payload': {fakeUser}
  };
  expect(rootReducer(previousState, logInAction)).toEqual({
    'userReducer': {
      loggedIn: true,
      user: { fakeUser }
    }
  });
});


it('log out action', () => {
  const fakeUser = {
    "pk": 1,
    "full_name": "Nikita Selin",
    "email": "nikita@selin.com.ru",
    "role": "administrator"
  };
  const previousState = {
    'userReducer': {
      loggedIn: true,
      user: {fakeUser}
    }
  };
  const logOutAction = {
    'type': 'LOG_OUT'
  };
  expect(rootReducer(previousState, logOutAction)).toEqual({
    'userReducer': {
      loggedIn: false,
      user: {}
    }
  });
});
