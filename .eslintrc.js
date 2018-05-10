module.exports = {
    extends: [
        'airbnb-base',
    ],
    parser: 'babel-eslint',
    rules: {
        'indent': [1, 4],
        'max-len': [1, 120, 2, {"ignoreComments": true}],
        'quote-props': [1, 'consistent-as-needed'],
        'semi': [0, 'never'],
    }
};
