import React from 'react';


const CourseCard = (props) => {
  const item = props.item;
  const isAdmin = props.isAdmin;
  return (
    <div className="col mb-4" id={item.id}>
      <div className="card">
        <a href="#" className="card-link">
          <img src={item.thumbnail} className="card-img-top" alt={item.title} />
        </a>
        <div className="card-body">
          <h5 className="card-title text-center">{item.title}</h5>
          {/* Superuser block */}
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
      {items.map((item) => <CourseCard item={item} isAdmin={isAdmin} key={item.id} />)}
    </div>
  )
}


class CoursesList extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            coursesListUrl: this.props.url,
            coursesList: [],
            isAdmin: false
        }
    }

    componentDidMount() {
      const url = this.state.coursesListUrl;
      let self = this;
      fetch(url)
      .then((response) => response.json())
          .then(function (data) {
              console.log(data);
              self.setState({ coursesList: data.results });
      })
      .catch(function (error) {
          console.log(error);
      });  
    }

    render() {
      return(
        <div className="container col-lg-6">
          <h1 className="text-center">Список курсов</h1>
          <hr />
            <AllCoursesCards items={this.state.coursesList} isAdmin={this.state.isAdmin} />
        </div>
      );
    }
}

export default CoursesList
