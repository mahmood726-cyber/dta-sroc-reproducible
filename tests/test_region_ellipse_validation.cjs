const test = require('node:test');
const assert = require('node:assert/strict');
const { regionEllipse } = require('../app/shared/dta-bivariate.js');
const base = (C) => ({muLogitSe:0.3,muLogitFPR:-0.4,covMu:C,Psi:[[0,0],[0,0]]});
test('rejects invalid covariance and malformed inputs', () => {
  for (const C of [ [[1,2],[2,1]], [[1,0.2],[0.1,1]], [[NaN,0],[0,1]], [[-1,0],[0,1]], [[1,0]], [] ]) {
    assert.throws(() => regionEllipse(base(C),'confidence',40), RangeError);
  }
  for (const n of [0,-2,2,2.4,Infinity,NaN]) assert.throws(() => regionEllipse(base([[1,0],[0,1]]),'confidence',n),RangeError);
  assert.throws(()=>regionEllipse(base([[1,0],[0,1]]),'wrong',40),RangeError);
  assert.throws(()=>regionEllipse({...base([[1,0],[0,1]]),muLogitSe:NaN},'confidence',40),RangeError);
});
test('finite and degenerate valid regions', () => {
  for(const C of [[[1,0.2],[0.2,2]],[[0,0],[0,1]],[[1,0],[0,0]],[[0,0],[0,0]]]){
    const pts=regionEllipse(base(C),'confidence',40);
    assert.equal(pts.length,41);
    assert.ok(pts.every(p=>Number.isFinite(p.tpr)&&Number.isFinite(p.fpr)&&p.tpr>=0&&p.tpr<=1&&p.fpr>=0&&p.fpr<=1));
  }
});
test('valid region determinism and default point count', () => {
 const f=base([[1,0.3],[0.3,2]]);
 assert.deepEqual(regionEllipse(f,'confidence',50),regionEllipse(f,'confidence',50));
 assert.equal(regionEllipse(f,'prediction').length,101);
});
