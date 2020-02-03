import React from 'react';
import EmptyListMessage from "./EmptyListMessage";

class CommitList extends React.Component {

    constructor(props) {
        super(props);
    }

    getDateTimeFormat(date) {
        const commitDate = new Date(date);
        return Intl.DateTimeFormat('en-GB', {
            weekday: 'short',
            month: 'short',
            day: '2-digit',
            hour: '2-digit',
            minute: '2-digit',
            second:'2-digit',
            timeZoneName: 'short'
        }).format(commitDate)
    }

    render(){
        const { commits } = this.props;
        return (
            commits ? (
                <div className="card">
                    {commits.map(commit => (
                        <div className="card-body commit bg-primary" key={commit.sha}>
                            <h4 className="card-title">commit {commit.sha}</h4>
                            <a href={`mailto:${commit.author_email}`} className="email-link">{commit.author_username} &lt;{commit.author_email}&gt;</a>
                            <p className="card-text">{commit.message}</p>
                            <p className="card-text">{this.getDateTimeFormat(commit.date)}</p>
                        </div>
                    ))}
                </div>
            ) : (
                <EmptyListMessage message="Select a repository" />
            )
        )
    }
}

export default CommitList;
