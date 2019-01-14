import React, { Component } from 'react';
import blueCarImgSrc from '../img/blue-car.png';
import orangeCarImgSrc from '../img/orange-car.png';
import ballImgSrc from '../img/ball.png';
import fieldImgSrc from '../img/field.png';

export default class Minimap extends Component {

    constructor(props) {
        super(props);

        // Start loading images now
        this.fieldImg = new Image();
        this.fieldImg.src = fieldImgSrc;
        this.ballImg = new Image();
        this.ballImg.src = ballImgSrc;
        this.blueCarImg = new Image();
        this.blueCarImg.src = blueCarImgSrc;
        this.orangeCarImg = new Image();
        this.orangeCarImg.src = orangeCarImgSrc;
    }

    componentDidMount() {
        this.updateCanvas();
    }

    componentDidUpdate() {
        this.updateCanvas();
    }

    updateCanvas() {
        const container = this.refs.container;
        const width = container.offsetWidth;
        const height = container.offsetHeight - 5; // Make sure the canvas doesn't force a resize of the container, which would trigger an infinite loop

        // Size the field as to best fit the canvas size
        const canvas = this.refs.canvas;
        canvas.width = width;
        canvas.height = height;

        let fieldImgX = 0;
        let fieldImgY = 0;
        let fieldImgWidth = this.fieldImg.naturalWidth;
        let fieldImgHeight = this.fieldImg.naturalHeight;
        const fieldImgAspectRatio = fieldImgWidth / fieldImgHeight;
        const canvasAspectRatio = width / height;
        if (canvasAspectRatio > fieldImgAspectRatio) { // The canvas is wider
            fieldImgHeight = height;
            fieldImgWidth = fieldImgHeight * fieldImgAspectRatio;
            fieldImgX = (width - fieldImgWidth) / 2;
        } else { // The image is wider
            fieldImgWidth = width;
            fieldImgHeight = fieldImgWidth / fieldImgAspectRatio;
            fieldImgY = (height - fieldImgHeight) / 2;
        }

        const ctx = canvas.getContext('2d');
        ctx.drawImage(this.fieldImg, fieldImgX, fieldImgY, fieldImgWidth, fieldImgHeight);

        this.props.bluePlayersState.forEach((car) => {
            this.drawImageFromGameState(ctx, this.blueCarImg, car.loc, car.rot.z, fieldImgWidth, fieldImgHeight, fieldImgX, fieldImgY);
        });
        this.props.orangePlayersState.forEach((car) => {
            this.drawImageFromGameState(ctx, this.orangeCarImg, car.loc, car.rot.z, fieldImgWidth, fieldImgHeight, fieldImgX, fieldImgY);
        });

        const ball = this.props.ballState;
        this.drawImageFromGameState(ctx, this.ballImg, ball.loc, 0, fieldImgWidth, fieldImgHeight, fieldImgX, fieldImgY);
    }

    drawImageFromGameState(ctx, image, gameLocation, rotAngle, maxWidth, maxHeight, rootX, rootY) {
        const { x, y } = this.translateGameToCanvasCoord(gameLocation.x, gameLocation.y, maxWidth, maxHeight, rootX, rootY);
        ctx.save();
        ctx.translate(x, y);
        ctx.rotate(rotAngle);
        ctx.drawImage(image, -image.width / 2, -image.height / 2);
        ctx.restore();
    }

    translateGameToCanvasCoord(gameCoordX, gameCoordY, maxWidth, maxHeight, rootX, rootY) {
        const { min_x, x_size, min_y, y_size } = this.props.fieldSize;
        // NOTE The game XY coordinates is inverted from this canvas' coordinate system
        return {
            x: (gameCoordY - min_y) / y_size * maxWidth + rootX,
            y: (gameCoordX - min_x) / x_size * maxHeight + rootY
        }
    }

    render() {
        // TODO this is where we can use something like a <canvas> to display a minimap
        // Other possibilities would be to render a small 3D scene using three.js
        // Or to use D3.js to easily map our data to an SVG output
        return (
            <div ref="container" className='minimap'>
                <canvas ref="canvas"></canvas>
            </div>
        );
    }
}
