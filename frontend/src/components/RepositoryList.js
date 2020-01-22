import React from 'react';

class RepositoryList extends React.Component {

    state = {
        activeId: null
    }

    mock() {
        return [
            {
                'id': 1,
                'name': 'blog_django',
                'description': 'Código usado para aprender Django',
            },
            {
                'id': 2,
                'name': 'blog_django',
                'description': 'Código usado para aprender Django',
            },
        ]
    }

    handleClick(e, id) {
        this.setState({activeId: id});
    }

    getActiveClass(repoId) {
        let className = "list-group-item list-group-item-action flex-column align-items-start repository";
        if(this.state.activeId == repoId) {
            className += ' active';
        }
        return className;
    }

    render() {
        const repositories = this.mock();
        return (
            <div className="list-group">
                {repositories.map(repo => (
                    <a
                    href="#"
                    className={this.getActiveClass(repo.id)}
                    onClick={this.handleClick.bind(this, repo.id)}
                    >
                        <div className="d-flex w-100 justify-content-between">
                            <h4 className="mb-1">{repo.name}</h4>
                        </div>
                        <p className="mb-1">{repo.description}</p>
                    </a>
                ))}
            </div>
        )
    }
}

export default RepositoryList;
