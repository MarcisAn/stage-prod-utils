import ws281x from 'rpi-ws281x-native';
const options = {
  dma: 10,
  freq: 800000,
  gpio: 18,
  invert: false,
  brightness: 255,
  stripType: ws281x.stripType.WS2812
};

const channel = ws281x(200, options);
const colors = channel.array;

import { WebSocketServer } from 'ws';

const wss = new WebSocketServer({ port: 8765 });

wss.on('connection', function connection(ws) {
  ws.on('error', console.error);

  ws.on('message', function message(data) {
    const array = JSON.parse(data)
        for (let i = 0; i< 200;i++){
                colors[i] = rgb2Int(array[i*3+1], array[i*3], array[i*3+2]);
        }
        ws281x.render();
  });

  ws.send('rr')
});

// update color-values
colors[199] = 0xffcc22;
ws281x.render();

function rgb2Int(r, g, b) {
  return ((r & 0xff) << 16) | ((g & 0xff) << 8) | (b & 0xff);
}