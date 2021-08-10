import React from 'react';
import { Link } from 'react-router-dom';
import CoursesService from './CoursesService';


const coursesService = new CoursesService();

const CourseCard = (props) => {
  const item = props.item;
  const isAdmin = props.isAdmin;
  return (
    <div className="col mb-4" id={item.id}>
      <div className="card">
        <Link to={"/courses/details/" + item.id + "/"} className="card-link">
          <img src={item.thumbnail} className="card-img-top" alt={item.title} />
        </Link>
        <div className="card-body">
          <h5 className="card-title text-center">{item.title}</h5>
          {/* Superuser block. 
              @ TODO! Get user role from redux fn add "Link" items for admin.
          */}
          {
            isAdmin === true
             ? (<p className="card-text text-center">
                  <a href="#" className="card-link">Редактировать</a>
                  <br />
                  <a href="#" className="card-link">Удалить</a>
                </p>)
             : null
          }
        </div>
      </div>
    </div>
  )
}

const AllCoursesCards = (props) => {
  const items = props.items;
  const isAdmin = props.isAdmin;
  return (
    <div className="row row-cols-1 row-cols-md-4">
      {items.map((item) => <CourseCard key={item.id} item={item} isAdmin={isAdmin} />)}
    </div>
  )
}

class CoursesList extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            coursesList: [],
            isAdmin: false,
            pageNumber: 1,
            nextPageURL: '',
            previousPageURL: '',
        };
        this.nearbyPage  =  this.nearbyPage.bind(this);
        this.nextPage  =  this.nextPage.bind(this);
        this.previousPage  =  this.previousPage.bind(this);
        document.title = 'Список курсов';
    }

  // @TODO! Handle errors.
  componentDidMount() {
    let self = this;
    coursesService.getCoursesList()
      .then((data) => {
        console.log(data);
        self.setState({ 
          coursesList: data.results,
          nextPageURL: data.next,
          previousPageURL: data.previous,
        }) 
      })
      .catch((error) => {
        console.log(error);
    });
  }

  nearbyPage(pageURL) {
    const url = new URL(pageURL);
    const urlParams = new URLSearchParams(url.search);
    const page = urlParams.get('page');
    this.setState({
      pageNumber: page ? page : 1,
    });
    let self = this;
    coursesService.getCoursesListByURL(pageURL)
      .then((data) => {
        self.setState({ 
          coursesList: data.results,
          nextPageURL: data.next,
          previousPageURL: data.previous,
        })
      })
      .catch((error) => {
        console.log(error);
    });
  }

  nextPage() {
    if (!this.state.nextPageURL) {
      return null;
    }
    this.nearbyPage(this.state.nextPageURL);
  }

  previousPage() {
    if (!this.state.previousPageURL) {
      return null;
    }
    this.nearbyPage(this.state.previousPageURL);
  }

  render() {
    return(
      <div className="container col-lg-6">
        <h1 className="text-center">Список курсов</h1>
        <hr />
        <AllCoursesCards items={this.state.coursesList} isAdmin={this.state.isAdmin} />
        <div className="text-center">
          <button className="btn btn-sm btn-dark" onClick={this.previousPage}>{"<<"}</button>
          <b> {this.state.pageNumber} </b>
          <button className="btn btn-sm btn-dark" onClick={this.nextPage}>{">>"}</button>
        </div>
      </div>
    );
  }
}

export default CoursesList;
export {
  CourseCard,
  AllCoursesCards
};