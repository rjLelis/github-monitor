import React from "react";

class RepositoryForm extends React.Component {

    render() {
        return (
            <form className="form-inline">
                <input className="form-control mr-sm-2 repo-input" type="text" placeholder="Add a repository to the monitor" />
                <button className="btn btn-primary my-2 my-sm-0" type="submit">Add</button>
            </form>
        )
    }
}

export default RepositoryForm;
