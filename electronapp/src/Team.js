import React, { Component } from 'react';

export default class Team extends Component {
    render() {
        const { team } = this.props;
        const teamColor = team === 1 ? 'Blue' : 'Orange';
        return (
            <div className={'team team-' + team}>{teamColor} Team</div>
        );
    }
}
