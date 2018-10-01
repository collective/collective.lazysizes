const HtmlWebpackPlugin = require('html-webpack-plugin')

// get partial prefix of latest commit in webpack directory
const childProcess = require('child_process');
const gitCmd = 'git rev-list -1 HEAD --abbrev-commit $(pwd)'
const gitHash = childProcess.execSync(gitCmd).toString().substring(0, 7);

// clean up old script
const path = `${__dirname}/../src/collective/lazysizes/browser/static`
childProcess.execSync(`rm -f ${path}/lazysizes-*`);

module.exports = {
  entry: [
    './app/lazysizes-icon.png',
    './app/lazysizes.js',
  ],
  output: {
    filename: `lazysizes-${gitHash}.js`,
    library: 'lazysizes',
    libraryTarget: 'umd',
    libraryExport: 'default',
    path: path,
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
  plugins: [
    new HtmlWebpackPlugin({
      inject: false,
      filename: 'resources.pt',
      template: 'app/resources.pt',
    })
  ]
}
