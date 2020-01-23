import React from "react";
import axios from 'axios';
import Header from './Header';
import RepositoryList from './RepositoryList';
import CommitList from './CommitList';
import RepositoryForm from "./RepositoryForm";

class App extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            repositories: [],
            commits: []
        };
    }

    componentDidMount() {
       axios.get('/api/repositories').then(response => {
           return response.data;
       }).then(data => this.setState({ repositories: data }));
    }

    handleClick(repoName) {
        axios.get(`/api/repositories/${repoName}/commits`).then(response => {
            return response.data;
        }).then(data => this.setState({ commits: data} ));
        console.log(this.state.commits)
    }

    render() {
        const { commits, repositories } = this.state;
        return (
            <div>
                <header className="site-header bd-navbar">
                    <Header />
                </header>
                <main role="main" className="jumbotron">
                    <div className="row">
                        <div className='col-md-12'>
                            <RepositoryForm />
                        </div>
                        <div className="col-md-4">
                            <RepositoryList
                                repositories={repositories}
                                onClick={(repoName) => this.handleClick(repoName)}
                            />
                        </div>
                        <div className="col-md-8">
                            <CommitList commits={commits} />
                        </div>
                    </div>
                </main>
            </div>
        )
    }
}

export default App;
