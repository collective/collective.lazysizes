const makeConfig = require('sc-recipe-staticresources');


module.exports = makeConfig(
  // name
  'collective.lazysizes',

  // shortName
  'lazysizes',

  // path
  `${__dirname}/../src/collective/lazysizes/browser/static`,

  //publicPath
  '++resource++collective.lazysizes/',

  //callback
  function(config, options) {
    config.entry.unshift(
      './app/lazysizes-icon.png',
    );
  },
);
