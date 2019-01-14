import React, { Component } from 'react';
import playImg from '../img/play3.png';
import pauseImg from '../img/pause.png';
import './Timeline.css';


const SLIDER_RANGE = 1000;

export default class Timeline extends Component {

    constructor(props) {
        super(props);

        this.handleSliderChange = this.handleSliderChange.bind(this);
    }

    handleSliderChange(e) {
        this.props.setPlaytimeTo(e.target.value / SLIDER_RANGE);
    }

    render() {
        const { play, pause, playing, playtimeFraction } = this.props;
        return (
            <div className='timeline'>
                <input className='slider' type='range' min='0' max={SLIDER_RANGE} value={playtimeFraction * SLIDER_RANGE} onChange={this.handleSliderChange}/>
                {playing ? (
                    <img className='play-pause-button' onClick={pause} src={pauseImg} alt='Pause' />
                ) : (
                    <img className='play-pause-button' onClick={play} src={playImg} alt='Play' />
                )}
            </div>
        );
    }
}
