export function isInnChecksumValid(inn: string): boolean {
  if (inn.length === 10) {
    const coeffs = [2, 4, 10, 3, 5, 9, 4, 6, 8];
    const control = coeffs.reduce((sum, c, i) => sum + c * Number(inn[i]), 0) % 11 % 10;
    return control === Number(inn[9]);
  }

  if (inn.length === 12) {
    const coeffs11 = [7, 2, 4, 10, 3, 5, 9, 4, 6, 8];
    const coeffs12 = [3, 7, 2, 4, 10, 3, 5, 9, 4, 6, 8];
    const control11 = coeffs11.reduce((sum, c, i) => sum + c * Number(inn[i]), 0) % 11 % 10;
    const control12 = coeffs12.reduce((sum, c, i) => sum + c * Number(inn[i]), 0) % 11 % 10;
    return control11 === Number(inn[10]) && control12 === Number(inn[11]);
  }

  return false;
}

export function isOgrnChecksumValid(ogrn: string): boolean {
  if (ogrn.length === 13) {
    return Number(BigInt(ogrn.slice(0, 12)) % 11n % 10n) === Number(ogrn[12]);
  }
  if (ogrn.length === 15) {
    return Number(BigInt(ogrn.slice(0, 14)) % 13n % 10n) === Number(ogrn[14]);
  }
  return false;
}
