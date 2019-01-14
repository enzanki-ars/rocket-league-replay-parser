import React, { Component } from 'react';
import './Scoreboard.css';
import logo from '../img/logo.png';

export default class Scoreboard extends Component {
    render() {
        const { nameBlue, nameOrange, timerMinutes, timerSeconds, scoreBlue, scoreOrange } = this.props;

        return (
            <div className='scoreboard'>
                <div>
                    <div className='scoreboard-team'>
                        <img src={logo} alt='blue-team-logo' />
                        <h2 className='team-name'>{nameBlue}</h2>
                    </div>
                    <div className='score-and-time'>
                        <div>
                            <div className='score score-blue'>{scoreBlue}</div>
                            <div className='timer'>{timerMinutes}:{timerSeconds}</div>
                            <div className='score score-orange'>{scoreOrange}</div>
                        </div>
                    </div>
                    <div className='scoreboard-team'>
                        <h2 className='team-name'>{nameOrange}</h2>
                        <img src={logo} alt='orange-team-logo' />
                    </div>
                </div>
            </div>
        );
    }
}
