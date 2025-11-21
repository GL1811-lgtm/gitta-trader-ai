function setupAgentsSocket(io) {
  const nsp = io.of('/agents/status');

  nsp.on('connection', (socket) => {
    console.log('Client connected to /agents/status');

    let interval;

    // Initial state of agents (can be loaded from a config or DB)
    const agents = [
      { id: 'Master-1', name: 'Master', status: 'Idle', activity: '', cpu: 0, memory: 0 },
      { id: 'Collector-01', name: 'Collector-01', status: 'Idle', activity: '', cpu: 0, memory: 0 },
      { id: 'Collector-02', name: 'Collector-02', status: 'Idle', activity: '', cpu: 0, memory: 0 },
      { id: 'Tester-01', name: 'Tester-01', status: 'Idle', activity: '', cpu: 0, memory: 0 },
      { id: 'Supervisor-01', name: 'Supervisor-01', status: 'Idle', activity: '', cpu: 0, memory: 0 },
      { id: 'Expert-01', name: 'Expert-01', status: 'Idle', activity: '', cpu: 0, memory: 0 },
    ];

    const sendStatus = () => {
      agents.forEach(a => {
        a.cpu = Math.round(Math.random() * 80 + 10); // 10-90%
        a.memory = Math.round(Math.random() * 80 + 10); // 10-90%

        const statuses = ['Processing', 'Fetching', 'Idle', 'Sleeping', 'Error'];
        a.status = statuses[Math.floor(Math.random() * statuses.length)];

        switch (a.status) {
          case 'Processing':
            a.activity = 'Compiling daily report...';
            break;
          case 'Fetching':
            a.activity = 'Ingesting 1-min tick data...';
            break;
          case 'Error':
            a.activity = 'Restarting due to an error...';
            break;
          default:
            a.activity = 'Waiting for tasks';
        }
      });
      socket.emit('agents', agents);
    };

    // Send initial status immediately
    sendStatus();

    interval = setInterval(sendStatus, parseInt(process.env.STOCK_TICK_INTERVAL_MS || '2500', 10));

    socket.on('disconnect', () => {
      console.log('Client disconnected from /agents/status');
      clearInterval(interval);
    });
  });
}

module.exports = {
  setupAgentsSocket
};