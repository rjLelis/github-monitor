import React from 'react'
import axios from 'axios';


class Paginator extends React.Component {

    constructor(props) {
        super(props);
    }

    onPageChange(e, url) {
        axios.get(url).then(response => {
            return response.data
        }).then(data => this.props.onPageChange('commits', data));
    }

    render() {
        const { current_page, previous, next } = this.props;
        return (
            next || previous ? (
                <div className='paginator'>
                    {previous && <a
                        className='btn btn-outline-info mb-4'
                        onClick={(e) => this.onPageChange(e, previous)}>
                            {current_page - 1}
                        </a>}
                    <a className='btn btn-outline-info mb-4' href='#'>
                        {current_page}
                    </a>
                    {next && <a
                        className='btn btn-outline-info mb-4'
                        onClick={(e) =>this.onPageChange(e, next)}>
                            {current_page + 1}
                        </a>}
                </div>
            ) : (
                <div></div>
            )
        )
    }
}

export default Paginator;
