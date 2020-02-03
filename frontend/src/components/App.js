import React from "react";
import axios from 'axios';
import Header from './Header';
import RepositoryList from './RepositoryList';
import CommitList from './CommitList';
import RepositoryForm from "./RepositoryForm";
import Paginator from './Paginator';

class App extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            repositories: [],
            commits: {},
        };
    }

    componentDidMount() {
       axios.get('/api/repositories').then(response => {
           return response.data;
       }).then(data => this.setState({ repositories: data }));
    }

    handleClick(repoName) {
        axios.get(`/api/repositories/${repoName}/commits?page=1`).then(response => {
            return response.data;
        }).then(data => this.setState({
            commits: data,
        }));
    }

    handleSubmit() {
        axios.get('/api/repositories').then(response => {
            return response.data;
        }).then(data => this.setState({ repositories: data }));
    }

    handlePageChange(object, results) {
        this.setState({
            [object]: results
        })
    }

    render() {
        const { commits, repositories } = this.state;
        const { results, current_page, next, previous } = commits;
        return (
            <div>
                <header className="site-header bd-navbar">
                    <Header />
                </header>
                <main role="main" className="jumbotron">
                    <div className="row">
                        <div className='col-md-12'>
                            <RepositoryForm
                                onSubmit={() => this.handleSubmit()}
                            />
                        </div>
                        <div className="col-md-4">
                            <RepositoryList
                                repositories={repositories}
                                onClick={(repoName) => this.handleClick(repoName)}
                            />
                        </div>
                        <div className="col-md-8">
                            <CommitList commits={results} />
                            <Paginator
                                current_page={current_page}
                                previous={previous}
                                next={next}
                                onPageChange={(object, results) => this.handlePageChange(object, results)}
                            />
                        </div>
                    </div>
                </main>
            </div>
        )
    }
}

export default App;
