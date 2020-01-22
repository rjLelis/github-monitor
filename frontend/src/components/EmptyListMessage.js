import React from 'react';

class EmptyListMessage extends React.Component {

    constructor(props) {
        super(props);
    }

    render() {
        const { message } = this.props
        return (
            <div className="card-body commit bg-primary">
                <h4 className="card-title">{message}</h4>
            </div>
        )
    }
}

export default EmptyListMessage;
