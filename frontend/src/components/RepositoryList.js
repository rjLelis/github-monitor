import React from 'react';
import EmptyListMessage from "./EmptyListMessage";

class RepositoryList extends React.Component {


    constructor(props) {
        super(props);
        this.state = {
            activeId: null
        }

        this.handleClick = this.handleClick.bind(this);
    }

    handleClick(e, id, repoName) {
        this.setState({activeId: id});
        this.props.onClick(repoName)
    }

    getActiveClass(repoId) {
        let className = "list-group-item list-group-item-action flex-column align-items-start repository";
        if(this.state.activeId === repoId) {
            className += ' active';
        }
        return className;
    }

    render() {
        const { repositories } = this.props;
        return (
            repositories.length > 1 ? (
                <div className="list-group">
                    {repositories.map(repo => (
                        <a
                            key={repo.id}
                            href="#"
                            className={this.getActiveClass(repo.id)}
                            onClick={(e) => this.handleClick(e, repo.id, repo.name)}
                        >
                            <div className="d-flex w-100 justify-content-between">
                                <h4 className="mb-1">{repo.name}</h4>
                            </div>
                            <p className="mb-1">{repo.description}</p>
                        </a>
                    ))}
                </div>
            ) : (
                <EmptyListMessage message="No repositories to show" />
            )
        )
    }
}

export default RepositoryList;
