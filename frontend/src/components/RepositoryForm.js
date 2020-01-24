import React from "react";
import axios from 'axios';
import FlashMessage from './FlashMessage';

class RepositoryForm extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            repository: "",
            message: "",
            messageType: ""
        }
    }

    handleClick(e) {
        return this.setState({ message: ""});
    }

    handleSubmit(e) {
        e.preventDefault();
        const { repository } = this.state;
        if(repository.trim() === '') {
            return this.setState(() => {
                return {
                    message: 'Enter the name of a repository',
                    messageType: 'danger'
                }
            });
        }
        axios.post('/api/repositories', {
            repository
        }).then(response => {
            const message = `${repository} is now monitored`
            this.setState({
                repository: "",
                message: message,
                messageType:'success'
            });
            this.props.onSubmit()
        }).catch(error => {
            return this.setState({
                message: error.response.data,
                messageType: 'danger'
            });
        })
    }

    handleChange(e) {
        this.setState({[e.target.name]: e.target.value});
    }

    render() {
        const { repository, message, messageType } = this.state;
        return (
            <form className="form-inline">
                <FlashMessage
                    handleClick={(e) => this.handleClick(e)}
                    message={message}
                    messageType={messageType}
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
