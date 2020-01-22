import React from 'react';

class Header extends React.Component {
    render() {
        return (
                <nav className="navbar navbar-expand-lg navbar-dark bg-primary">
                    <a className="navbar-brand" href="#">Github Monitor</a>
                    <button className="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarColor01" aria-controls="navbarColor01" aria-expanded="false" aria-label="Toggle navigation">
                        <span className="navbar-toggler-icon"></span>
                    </button>

                    <div className="collapse navbar-collapse flex-end" id="navbarColor01">
                        <ul className="navbar-nav">
                            <li className="nav-item my-2 my-lg-0" >
                                <a className="nav-link" href="/auth/logout">Logout</a>
                            </li>
                        </ul>
                        {/* <form className="form-inline my-2 my-lg-0">
                            <input className="form-control mr-sm-2" type="text" placeholder="Search" />
                            <button className="btn btn-secondary my-2 my-sm-0" type="submit">Search</button>
                        </form> */}
                    </div>
                </nav>
        )
    }
}

export default Header;
