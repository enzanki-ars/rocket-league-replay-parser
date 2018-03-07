import React, { Component } from 'react';
import logo from '../img/logo.png';
import './Player.css';

export default class Player extends Component {
    render() {
        const { info } = this.props;
        return (
            <div className='player-info'>
                <div className='player-photo'>
                    <img src={logo} alt='blue-team-logo' />
                </div>
                <div className='player-name'>{info.name}</div>
                <div className='player-goals'>
                    <div className='player-stat-title'>Goals</div>
                    <div>{info.goals}</div>
                </div>
                <div className='player-assists'>
                    <div className='player-stat-title'>Assists</div>
                    <div>{info.assists}</div>
                </div>
                <div className='player-saves'>
                    <div className='player-stat-title'>Saves</div>
                    <div>{info.saves}</div>
                </div>
                <div className='player-shots'>
                    <div className='player-stat-title'>Shots</div>
                    <div>{info.saves}</div>
                </div>
            </div>
        );
    }
}
