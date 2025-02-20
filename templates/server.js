db.query('SELECT NOW()', (err, results) => {
    if (err) {
      console.error('Database query failed:', err);
      return;
    }
    console.log('Database is connected:', results);
  });
  const PORT = 3000; // Change to an unused port
