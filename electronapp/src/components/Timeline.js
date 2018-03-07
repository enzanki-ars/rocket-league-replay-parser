import React, { Component } from 'react';

export default class Timeline extends Component {
    render() {
        const { play, pause, playing } = this.props;
        return (
            <div className='timeline'>
                Timeline
                {playing ? (
                    <button onClick={pause}>Pause</button>
                ) : (
                    <button onClick={play}>Play</button>
                )}
            </div>
        );
    }
}
