import React from 'react';

class CommitList extends React.Component {

    state = {
        commits: [],
    }

    mock() {
        const commits = [
        {
            sha: '238e871aa4946813f143fec27d2605ce734358ed',
            author_username: 'rjLelis',
            author_email: 'renatojlelis@gmail.com',
            message: 'Upgrade django',
            date: 'Sep 20, 2019'
        },
        {
            sha: '238e871aa4946813f143fec27d2605ce734358ed',
            author_username: 'rjLelis',
            author_email: 'renatojlelis@gmail.com',
            message: 'Upgrade django',
            date: 'Sep 20, 2019'
        },
        {
            sha: '238e871aa4946813f143fec27d2605ce734358ed',
            author_username: 'rjLelis',
            author_email: 'renatojlelis@gmail.com',
            message: 'Upgrade django',
            date: 'Sep 20, 2019'
        },
        {
            sha: '238e871aa4946813f143fec27d2605ce734358ed',
            author_username: 'rjLelis',
            author_email: 'renatojlelis@gmail.com',
            message: 'Upgrade django',
            date: 'Sep 20, 2019'
        },
        {
            sha: '238e871aa4946813f143fec27d2605ce734358ed',
            author_username: 'rjLelis',
            author_email: 'renatojlelis@gmail.com',
            message: 'Upgrade django',
            date: '2020-01-21T23:45:00.000Z'
        },
        ]
        return commits;
    }

    componentDidMount() {
        const request = {
            data: this.mock()
        }
        this.setState({ commit: request.data })

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
        const commits = this.mock();
        return (
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
        )
    }
}

export default CommitList;
