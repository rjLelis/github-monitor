import React from "react";
import Header from './Header';
import RepositoryList from './RepositoryList';
import CommitList from './CommitList';

class App extends React.Component {

    render() {
        return (
            <div>
                <header className="site-header">
                    <Header />
                </header>
                <main role="main" className="jumbotron">
                    <div className="row">
                        <div className="col-md-4">
                            <RepositoryList />
                        </div>
                        <div className="col-md-8">
                            <CommitList />
                        </div>
                    </div>
                </main>
            </div>
        )
    }
}

export default App;
