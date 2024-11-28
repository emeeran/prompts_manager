module.exports = {
  entry: './app/static/js/sidebar.jsx',
  output: {
    filename: 'bundle.js',
    path: __dirname + '/app/static/js',
  },
  module: {
    rules: [
      {
        test: /\.jsx?$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: ['@babel/preset-react'],
          },
        },
      },
    ],
  },
};
