import React from 'react';

class FlashMessage extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            message: ""
        }
    }

    componentDidMount() {
        const { message } = this.props;
        return this.setState({ message: message });
    }

    getMessageType() {
        const { messageType } = this.props;
        const className = `alert alert-dismissible alert-${messageType}`;
        return className;
    }

    render() {
        const { message } = this.props;
        return (
            message === "" ? "" :
            (<div className={this.getMessageType()}>
                <button
                    onClick={(e) => this.props.handleClick(e)}
                    type="button"
                    className="close"
                    data-dismiss="alert">
                        &times;
                </button>
                <div>{message}</div>
            </div>)
        )
    }
}

export default FlashMessage;
