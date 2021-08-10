import React from 'react';
import { MemoryRouter } from 'react-router-dom';

import { render, unmountComponentAtNode } from 'react-dom';
import { act } from 'react-dom/test-utils';

import CoursesList from './CoursesList';
import {
  CourseCard,
  AllCoursesCards,
} from './CoursesList';


const fakeCourse = {
  "id": 68,
  "course_group": [],
  "thumbnail": "http://127.0.0.1:8000/media/course/image.png.200x200_q85_crop-smart.jpg",
  "teachers": [],
  "title": "Test",
  "description": "Test test test",
  "image": "http://127.0.0.1:8000/media/course/image.png"
};

const fakeCoursesList = [
  {
    "id": 1,
    "course_group": [],
    "thumbnail": "http://127.0.0.1:8000/media/course/image.png.200x200_q85_crop-smart.jpg",
    "teachers": [],
    "title": "Test1",
    "description": "Test 1 1 1",
    "image": "http://127.0.0.1:8000/media/course/image.png"
  },
  {
    "id": 2,
    "course_group": [],
    "thumbnail": "http://127.0.0.1:8000/media/course/image.png.200x200_q85_crop-smart.jpg",
    "teachers": [],
    "title": "Test2",
    "description": "Test 2 2 2",
    "image": "http://127.0.0.1:8000/media/course/image.png"
  }
];


let container = null;

beforeEach(() => {
  // setup a DOM element as a render target
  container = document.createElement('div');
  document.body.appendChild(container);
});

afterEach(() => {
  // cleanup on exiting
  unmountComponentAtNode(container);
  container.remove();
  container = null;
});


it('render reference course card', () => {
  // Admin has full access
  act(() => {
    render(<MemoryRouter> <CourseCard item={fakeCourse} isAdmin={true} /> </MemoryRouter>, container);
  });
  expect(container.textContent).toContain(fakeCourse.title);
  expect(container.textContent).toContain('Редактировать');
  expect(container.textContent).toContain('Удалить');

  // Ordinary user
  act(() => {
    render(<MemoryRouter> <CourseCard item={fakeCourse} isAdmin={false} /> </MemoryRouter>, container);
  });
  expect(container.textContent).toContain(fakeCourse.title);
  expect(container.textContent).not.toContain('Редактировать');
  expect(container.textContent).not.toContain('Удалить');
});


it('render all reference course cards', () => {
  // Ordinary user
  act(() => {
    render(<MemoryRouter> <AllCoursesCards items={fakeCoursesList} isAdmin={false} /> </MemoryRouter>, container);
  });

  fakeCoursesList.map((fakeCourse) => {
    expect(container.textContent).toContain(fakeCourse.title);
  });
  expect(container.textContent).not.toContain('Редактировать');
  expect(container.textContent).not.toContain('Удалить');
});


it('render empty courses list', () => {
  act(() => {
    render(<CoursesList />, container);
  });
  expect(container.textContent).toBe('Список курсов<< 1 >>');
});
