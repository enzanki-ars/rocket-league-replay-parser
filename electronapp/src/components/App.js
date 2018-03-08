import React, { Component } from 'react';
import Team from './Team';
import Minimap from './Minimap';
import Timeline from './Timeline';
import Scoreboard from './Scoreboard';
import './App.css';

export default class App extends Component {

    constructor(props) {
        super(props);

        this.state = {
            players: {
                orange: {}, // Map of playerID to player data
                blue: {}
            },
            teams: {
                orange: {
                    name: '',
                    score: 0
                },
                blue: {
                    name: '',
                    score: 0
                }
            },
            frame: [],
            time: {
                minutes: 0,
                seconds: 0
            },

            ballState: {
                loc: {
                    x: 0,
                    y: 0
                }
            },
            bluePlayersState: [],
            orangePlayersState: [],
            fieldSize: {
                min_x: 0,
                min_y: 0,
                x_size: 0,
                y_size: 0 
            },

            playing: false
        };

        this.frames = [];
        this.currentFrame = 0;

        this.play = this.play.bind(this);
        this.pause = this.pause.bind(this);
        this.setPlaytimeTo = this.setPlaytimeTo.bind(this);
    }

    componentDidMount() {
        fetch('http://localhost:5000').then((response) => {
            return response.json();
        }).then((data) => {
            this.parseServerResponse(data);
        }).catch((error) => {
            console.error(`An error occured while fetching data: ${error.message}`);
        });
    }

    parseServerResponse(data) {
        console.log(data);
        this.frames = data.frames;

        // Initially:
        const newState = JSON.parse(JSON.stringify(this.state)); // Clone the state

        Object.keys(data.player_info).forEach((playerKey) => {
            const playerInfo = data.player_info[playerKey];
            if (playerInfo.team === 0) {
                newState.players.blue[playerKey] = playerInfo;
            } else {
                newState.players.orange[playerKey] = playerInfo;
            }
        });

        newState.teams.blue.name = data.team_info[0].name;
        newState.teams.orange.name = data.team_info[1].name;

        newState.fieldSize = data.field_size;

        this.setState(newState, () => {
            this.play(); // TODO Should this be removed and users have to press 'Play' manually?
        });
    }

    nextFrame() {
        // Every frame:
        const newState = JSON.parse(JSON.stringify(this.state)); // Clone the state

        const frame = this.frames[this.currentFrame];
        const { scoreboard, time, cars, ball } = frame;

        newState.teams.blue.score = scoreboard.team0;
        newState.teams.orange.score = scoreboard.team1;
        newState.time.minutes = time.game_minutes;
        newState.time.seconds = time.game_seconds;

        newState.ballState = ball;
        newState.bluePlayersState = [];
        newState.orangePlayersState = [];

        Object.keys(cars).forEach((playerID) => {
            const playerInfo = cars[playerID];
            const isBlueTeam = newState.players.blue[playerID] !== undefined;
            const player = isBlueTeam ? newState.players.blue[playerID]: newState.players.orange[playerID];
            Object.assign(player, playerInfo.scoreboard); // Player Stats

            // Player car state
            if (isBlueTeam) {
                newState.bluePlayersState.push(playerInfo);
            } else {
                newState.orangePlayersState.push(playerInfo);
            }
        });

        this.setState(newState, () => {
            if (this.state.playing) {
                setTimeout(() => {
                    if (this.currentFrame < this.frames.length - 1) {
                        this.currentFrame++;
                    }
                    this.nextFrame();
                }, time.replay_delta * 1000);
            }
        });
    }

    play() {
        if (!this.state.playing) {
            this.setState({ playing: true }, () => this.nextFrame());
        }
    }

    pause() {
        this.setState({ playing: false });
    }

    /**
     * Set the time of the playback from a specific time
     * @param {number} timeFraction value from 0 to 1, 0 being the start of the replay to 1 being the end
     */
    setPlaytimeTo(timeFraction) {
        if (!this.frames) {
            return;
        }
        
        this.currentFrame = Math.round((this.frames.length - 1) * timeFraction);
        if (!this.state.playing) { // Playback 1 frame in order to update the cars and player locations
            this.nextFrame();
        }
    }

    render() {
        const bluePlayers = Object.values(this.state.players.blue);
        const orangePlayers = Object.values(this.state.players.orange);
        const timerSeconds = ("0" + this.state.time.seconds).slice(-2); // Make sure 2 digits are shown
        const playtimeFraction = this.currentFrame / (this.frames.length - 1);
        return (
            <div className='App'>
                <Scoreboard
                    nameBlue={this.state.teams.blue.name}
                    nameOrange={this.state.teams.orange.name}
                    timerMinutes={this.state.time.minutes}
                    timerSeconds={timerSeconds}
                    scoreBlue={this.state.teams.blue.score}
                    scoreOrange={this.state.teams.orange.score}
                />
                <Minimap
                    ballState={this.state.ballState}
                    bluePlayersState={this.state.bluePlayersState}
                    orangePlayersState={this.state.orangePlayersState}
                    fieldSize={this.state.fieldSize}
                />
                <Team team='blue' players={bluePlayers} />
                <Team team='orange' players={orangePlayers} />
                <Timeline
                    play={this.play}
                    pause={this.pause}
                    setPlaytimeTo={this.setPlaytimeTo}
                    playing={this.state.playing}
                    playtimeFraction={playtimeFraction}
                />
            </div>
        );
    }
}

// const bluePlayers = [
        //     {
        //         name: 'Turbopolsa',
        //         goals: 1,
        //         assists: 0,
        //         saves: 2,
        //         shots: 2
        //     },
        //     {
        //         name: 'Kaydop',
        //         goals: 0,
        //         assists: 1,
        //         saves: 4,
        //         shots: 1
        //     },
        //     {
        //         name: 'ViolentPanda',
        //         goals: 1,
        //         assists: 1,
        //         saves: 1,
        //         shots: 4
        //     }
        // ];
        // const orangePlayers = [
        //     {
        //         name: 'Metsanauris',
        //         goals: 1,
        //         assists: 0,
        //         saves: 2,
        //         shots: 2
        //     },
        //     {
        //         name: 'Al0t',
        //         goals: 0,
        //         assists: 1,
        //         saves: 4,
        //         shots: 1
        //     },
        //     {
        //         name: 'Mognus',
        //         goals: 1,
        //         assists: 1,
        //         saves: 1,
        //         shots: 4
        //     }
        // ];
