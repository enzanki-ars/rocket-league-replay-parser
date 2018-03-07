import React, { Component } from 'react';
import Player from './Player';
import './Team.css';

export default class Team extends Component {
    render() {
        const { team, players } = this.props;
        return (
            <div className={'team team-' + team}>
                {players.map((player, key) =>
                    <Player info={player} key={key} />
                )}
            </div>
        );
    }
}
