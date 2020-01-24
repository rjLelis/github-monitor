import React from "react";
import axios from 'axios';
import FlashMessage from './FlashMessage';

class RepositoryForm extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            repository: "",
            submitErrorMessage: ""
        }
    }

    handleClick(e) {
        return this.setState({ submitErrorMessage: ""});
    }

    handleSubmit(e) {
        e.preventDefault();
        const { repository } = this.state;
        if(repository.trim() === '') {
            return this.setState(() => {
                return {
                    submitErrorMessage: 'Enter the name of a repository'
                }
            });
        }
        axios.post('/api/repositories', {
            repository
        }).then(response => {
            this.props.handleSubmit()
        }).catch(error => {
            return this.setState({
                submitErrorMessage: error.response.data
            });
        })
    }

    handleChange(e) {
        this.setState({[e.target.name]: e.target.value});
    }

    render() {
        const { repository, submitErrorMessage } = this.state;
        return (
            <form className="form-inline">
                <FlashMessage
                    handleClick={(e) => this.handleClick(e)}
                    message={submitErrorMessage}
                    messageType="danger"
                />
                <input
                    className="form-control mr-sm-2 repo-input"
                    type="text"
                    placeholder="Add a repository to the monitor"
                    name="repository"
                    onChange={(e) => this.handleChange(e)}
                    value={repository}
                />

                <button
                    className="btn btn-primary my-2 my-sm-0"
                    type="submit"
                    onClick={(e) => this.handleSubmit(e)}>
                        Add
                </button>
            </form>
        )
    }
}

export default RepositoryForm;
