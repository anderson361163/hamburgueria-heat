function phoneIsValid(phone) {
    const regex = /^(\([1-9]{2}\)|[1-9]{2})\s?[9]?[\d]{4}-?[\d]{4}$/;
    const phoneMathces = phone.match(regex);

    return  phoneMathces !== null;
}

function cepIsValid(cep) {
    const regex = /^[\d]{5}-?[\d]{3}$/;
    const cepMatches = cep.match(regex);
    
    return  cepMatches !== null;
}

function cpfIsValid(cpf) {
    if((cpf = cpf.replace(/[^\d]/g,'')).length !== 11) return false;

    if (
        cpf === '00000000000' ||
        cpf === '11111111111' ||
        cpf === '22222222222' || 
        cpf === '33333333333' ||
        cpf === '44444444444' ||
        cpf === '55555555555' ||
        cpf === '66666666666' ||
        cpf === '77777777777' ||
        cpf === '88888888888' ||
        cpf === '99999999999'
    ) return false;

    let result;
    let sum = 0;

    for (i = 1; i <= 9; i++) sum += parseInt(cpf[i - 1]) * (11 - i);

    result = (sum * 10) % 11;

    if ((result === 10) || (result === 11)) result = 0;

    if (result !== parseInt(cpf[9])) return false;

    sum = 0;

    for (i = 1; i <= 10; i++) sum += parseInt(cpf[i - 1]) * (12 - i);

    result = (sum * 10) % 11;

    if ((result === 10) || (result === 11)) result = 0;

    if (result !== parseInt(cpf[10])) return false;

    return true;
}

function addressNumberIsValid(number) {
    const regex = /^[\d]+$/
    const numerMatches = number.match(regex);

    return numerMatches !== null;
}
