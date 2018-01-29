module.exports = {
  entry: [
    './app/lazysizes-icon.png',
    './app/lazysizes.js',
  ],
  output: {
    filename: 'lazysizes.js',
    library: 'lazysizes',
    libraryTarget: 'umd',
    path: `${__dirname}/../src/collective/lazysizes/static`,
    publicPath: '++resource++collective.lazysizes/',
  },
  module: {
    rules: [{
      test: /\.js$/,
      exclude: /(\/node_modules\/|test\.js$|\.spec\.js$)/,
      use: 'babel-loader',
    }, {
      test: /.*\.(gif|png|jpe?g)$/i,
      use: [
        {
          loader: 'file-loader',
          options: {
            name: '[path][name].[ext]',
            context: 'app/',
          }
        },
        {
          loader: 'image-webpack-loader',
          query: {
            mozjpeg: {
              progressive: true,
            },
            pngquant: {
              quality: '65-90',
              speed: 4,
            },
            gifsicle: {
              interlaced: false,
            },
            optipng: {
              optimizationLevel: 7,
            }
          }
        }
      ]
    }]
  },
  devtool: 'source-map',
}
