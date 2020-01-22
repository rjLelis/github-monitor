import React from 'react';

class RepositoryList extends React.Component {

    state = {
        repositories: [],
        activeId: null
    }

    mock() {
        return [
            {
                id: 1,
                name: 'blog_django',
                description: 'Código usado para aprender Django',
                full_name: 'rjLelis/blog_django'
            },
            {
                id: 2,
                name: 'blog_django',
                description: 'Código usado para aprender Django',
                full_name: 'rjLelis/blog_django'
            },
        ]
    }

    componentDidMount() {
        const request = {
            data: this.mock()
        }
        this.setState({repositories: request.data})
    }

    handleClick(e, id, full_name) {
        this.setState({activeId: id});
    }

    getActiveClass(repoId) {
        let className = "list-group-item list-group-item-action flex-column align-items-start repository";
        if(this.state.activeId === repoId) {
            className += ' active';
        }
        return className;
    }

    render() {
        const { repositories } = this.state;
        return (
            <div className="list-group">
                {repositories.map(repo => (
                    <a
                        key={repo.id}
                        href="#"
                        className={this.getActiveClass(repo.id)}
                        onClick={(e) => this.handleClick(e, repo.id, repo.full_name)}
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
