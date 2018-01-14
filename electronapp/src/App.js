import React, { Component } from 'react';
import Team from './Team';
import Minimap from './Minimap';
import Timeline from './Timeline';
import Scoreboard from './Scoreboard';
import './App.css';

export default class App extends Component {
    render() {
        return (
            <div className="App">
                <Scoreboard />
                <Minimap />
                <Team team={1} />
                <Team team={2} />
                <Timeline />
            </div>
        );
    }
}
