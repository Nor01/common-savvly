/* eslint-disable tailwindcss/no-custom-classname */
// Calculator

import 'react-block-ui/style.css';

import * as numeral from 'numeral';

// import Image from 'next/image';
import { cloneDeep, debounce } from 'lodash';
import toast, { Toaster } from 'react-hot-toast';

// import ClipLoader from "react-spinners/ClipLoader";
// import LoadingOverlay from 'react-loading-overlay';
// import { css } from "@emotion/react";
import BlockUi from 'react-block-ui';
import { Component } from 'react';

// import logo from '../../styles/images/logo-white.png';

const axios = require('axios').default;

// import { AppConfig } from '@/utils/AppConfig';
//
// type IMainProps = {
//   meta: ReactNode;
//   children: ReactNode;
// };
//
// const Main = (props: IMainProps) => (
//   <div className="w-full px-1 text-gray-700 antialiased">
//     {props.meta}
//
//     <div className="mx-auto max-w-screen-md">
//       <div className="border-b border-gray-300">
//         <div className="pt-16 pb-8">
//           <div className="text-3xl font-bold text-gray-900">
//             {AppConfig.title}
//           </div>
//           <div className="text-xl">{AppConfig.description}</div>
//         </div>
//         <div>
//           <ul className="flex flex-wrap text-xl">
//             <li className="mr-6">
//               <Link href="/">
//                 <a className="border-none text-gray-700 hover:text-gray-900">
//                   Home
//                 </a>
//               </Link>
//             </li>
//             <li className="mr-6">
//               <Link href="/about/">
//                 <a className="border-none text-gray-700 hover:text-gray-900">
//                   About
//                 </a>
//               </Link>
//             </li>
//             <li className="mr-6">
//               <a
//                 className="border-none text-gray-700 hover:text-gray-900"
//                 href="https://github.com/ixartz/Next-js-Boilerplate"
//               >
//                 GitHub
//               </a>
//             </li>
//           </ul>
//         </div>
//       </div>
//
//       <div className="content py-5 text-xl">{props.children}</div>
//
//       <div className="border-t border-gray-300 py-8 text-center text-sm">
//         © Copyright {new Date().getFullYear()} {AppConfig.title}. Powered with{' '}
//         <span role="img" aria-label="Love">
//           ♥
//         </span>{' '}
//         by <a href="https://creativedesignsguru.com">CreativeDesignsGuru</a>
//         {/*
//          * PLEASE READ THIS SECTION
//          * We'll really appreciate if you could have a link to our website
//          * The link doesn't need to appear on every pages, one link on one page is enough.
//          * Thank you for your support it'll mean a lot for us.
//          */}
//       </div>
//     </div>
//   </div>
// );

/// /////////////////////////////////////////////////////////////////////////////

// const override = css`
//   display: block;
//   margin: 0 auto;
//   border-color: red;
//
// `;

// const debug = true;
const debug = false;

type Dimension = 'vertical' | 'horizontal';

interface IState {
  gender: string;
  currentAge: number;
  avgReturn: number;
  monthlyInstallment: number;
  retirementAge: number;
  calcInput: number;
  fundingAmnt: number;
  fundingAmntShow: number | string;
  chartDimension: Dimension;
  baseProspects: IProspect[];
  maxWithSavvly: number;
  maxWithOutSavvly: number;
  userProspect: IProspect;
  loading: boolean;
  isLoggedIn: boolean;
  password: string;
}

// interface Iarrayed {
//   data: any;
// }

interface IProspect {
  average_return: number;
  current_age: number;
  current_gender: string;
  funding_amount: number;
  monthly_installment: number;
  multiplier: string;
  name: string;
  payout_age: number;
  retirement_age: number;
  with_savvly: number;
  without_savvly: number;
}
// const Main = (props: any) => (

const withSavvlyMaxWidth = 406;
// const withoutSavvlyMaxWidth = 146;

export default class Calculator extends Component {
  constructor(props: any) {
    super(props);
    // if (debug) console.log('this constructor', this);
    this.state = {
      gender: 'Male',
      currentAge: 60,
      avgReturn: 6,
      monthlyInstallment: 0,
      retirementAge: 0,
      calcInput: 70,
      fundingAmnt: 175000,
      fundingAmntShow: '175000',
      baseProspects: [],
      userProspect: {} as IProspect,
      maxWithSavvly: 0,
      maxWithOutSavvly: 0,
      chartDimension: 'horizontal',
      loading: false,
      isLoggedIn: false,
      password: '',
    } as IState;

    this.getProspectCalculation = this.getProspectCalculation.bind(this);
    this.validateSearch = this.validateSearch.bind(this);
    // this.handleChange = debounce(this.handleChange.bind(this), 200);
    // this.searchCallbacks = []
  }

  searchCallbacks: any[] = [];

  componentDidMount() {
    this.handleSearch();
  }

  // handleChange(...args): any {
  //   console.log('---->hadleChange wrapper args', args);
  //   return debounce(this.handleChange_(...args), 500);
  //   // (event) => {
  //   //   console.log('---->1111111111111hadleChange wrapper funct args', event);
  //   //   // debounce(this.handleChange_(...args), 500);
  //   //   this.handleChange_(...args);
  //   // }
  // }

  handleChange(name: any, currentValue: any = null) {
    return (event: any) => {
      if (debug) console.log('name', name);
      if (debug) console.log('event', event);
      // if (debug) console.log('value', event.target.value);
      let nextPartialState: any = {};
      const { value } = event.target;
      if (debug) console.log('name value', value);
      switch (name) {
        case 'fundingAmntOptions':
          nextPartialState = { fundingAmnt: currentValue, fundingAmntShow: '' };
          break;
        case 'fundingAmnt': {
          const clearString = value.replace('$', '').replaceAll(',', '');
          const transformValue = Number(clearString);
          // console.log('clearString', clearString);
          // console.log('transformValue', transformValue);
          nextPartialState = {
            [name]: transformValue,
            fundingAmntShow: transformValue,
          };
          break;
        }
        case 'gender':
          nextPartialState = {
            gender: currentValue === 'Male' ? 'Female' : 'Male',
          };
          break;
        default:
          nextPartialState = { [name]: Number(value) ? Number(value) : '' };
          const resetValueCond =
            (name === 'avgReturn' && value.length > 2) ||
            (name === 'currentAge' && value.length > 2) ||
            (name === 'calcInput' && value.length > 2);
          if (resetValueCond) {
            const { state } = this;
            const { avgReturn, currentAge, calcInput } = state as IState;
            if (name === 'avgReturn') nextPartialState[name] = avgReturn;
            else if (name === 'currentAge') nextPartialState[name] = currentAge;
            else if (name === 'calcInput') nextPartialState[name] = calcInput;
          }
          break;
      }

      // if (debug) console.log('nextPartialState', nextPartialState);
      // const isValidSearch = this.validateSearch(nextPartialState, false)
      // if (isValidSearch) {
      //   nextPartialState = { ...nextPartialState, loading: true }
      // }
      // const callback = isValidSearch
      //   ? this.handleSearch1(name === 'calcInput')
      //   : null;
      const callback = debounce(
        this.handleCallback(cloneDeep(nextPartialState), name),
        1000
      );
      // const callback = debounce(this.handleCallback(nextPartialState, name), 1000, { leading: false, maxWait: 10000, trailing: true });

      this.searchCallbacks.push(callback);
      if (this.searchCallbacks.length > 1) {
        // this.searchCallbacks.forEach(_callback => _callback.cancel());
        // this.searchCallbacks = [];

        const previous = this.searchCallbacks.shift();
        // console.log('clone deep callbacks', cloneDeep(this.searchCallbacks))
        previous.cancel();
      }
      // if (!isValidSearch) {
      //   if (this.searchCallbacks.length > 0) {
      //     // this.searchCallbacks.forEach(_callback => _callback.cancel());
      //     // this.searchCallbacks = [];
      //
      //     this.searchCallbacks.push(callback);
      //     const previous = this.searchCallbacks.shift();
      //     previous.cancel();
      //   }
      //   else {
      //     this.searchCallbacks.push(callback);
      //   }
      // }
      // const handleCallback = isValidSearch
      //   ? callback
      //   : () => null;
      // this.setState(nextPartialState, callback);
      this.setState(nextPartialState, callback);
      //
      // if (isValidSearch) {
      //   this.handleSearch(name === 'calcInput')
      // }
    };
  }

  handleCallback(nextPartialState: Partial<IState>, name: string): any {
    return async () => {
      // console.log('------', a, b, c);
      const isValidSearch = this.validateSearch(nextPartialState);
      if (isValidSearch) {
        // nextPartialState = { ...nextPartialState, loading: true }
        this.setState({ loading: true });
        toast.dismiss();
        await this.handleSearch(name === 'calcInput');
      }
      // else {
      //   const previous = this.searchCallbacks.shift();
      //   console.log('previous', previous);
      //   console.log('previous', previous);
      //   previous.cancel();
      //   // console.log('previous', previous);
      // }
    };
  }

  getProspectCalculation(queryParams: {
    [key: string]: string;
  }): Promise<IProspect> {
    const options = {
      mode: 'no-cors',
      headers: {
        'Content-Type': 'application/json',
        'Allow-Origin': '*',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
        'Access-Control-Allow-Headers': 'Origin, Content-Type, X-Auth-Token',
      },
    };

    const baseUrl = 'https://simulator-dev-eastus.azurewebsites.net/calculator';
    const url = `${baseUrl}?${new URLSearchParams(queryParams)}`;

    return new Promise((resolve) => {
      axios
        .get(url, options)
        .then((response: any) => {
          if (debug) console.log('handleSearch response', response);
          if (response.status === 200) {
            resolve(response.data);
          } else {
            throw new Error('server error');
          }
        })
        .catch(() => {
          resolve({} as IProspect);
        });
    });
  }

  validateSearch(nextPartialState: any, notification = true): boolean {
    // let result = true;
    const { state } = this;
    const nextState = { ...state, ...nextPartialState };
    const {
      currentAge,
      calcInput,
      // currentAge, avgReturn, calcInput, fundingAmnt
    } = nextState as IState;

    const rulesDict: { [key: string]: any } = {
      currentAge: {
        range: [18, 80],
        label: 'Current Age',
      },
      calcInput: {
        range: [40, 90],
        label: 'Payout Age',
      },
      avgReturn: {
        range: [1, 100],
        label: 'Avg. Return',
      },
      fundingAmnt: {
        gte: 10000,
        label: 'Funding Amount',
      },
    };

    // const currentAgeCond = currentAge >= 18 && currentAge <= 90;
    // const calcInputCond = calcInput >= 40 && calcInput <= 90;
    // const avgReturnCond = avgReturn >= 1 && avgReturn <= 100;
    // const fundingAmntCond = fundingAmnt >= 10000;
    // const extraCond = currentAge < calcInput;
    let errorMessages: string[] = [];
    Object.keys(rulesDict).forEach((key: string) => {
      const value = nextState[key];
      const rulesInfo = rulesDict[key];
      const isRange =
        'range' in rulesInfo &&
        Array.isArray(rulesInfo.range) &&
        rulesInfo.range.length === 2;
      const isGte = 'gte' in rulesInfo;
      if (debug) console.log('key', key);
      if (debug) console.log('value', value);
      if (debug) console.log('isRange', isRange);
      if (debug) console.log('isGte', isGte);
      if (isRange) {
        const cond = value >= rulesInfo.range[0] && value <= rulesInfo.range[1];
        if (debug) console.log('cond', cond);
        if (!cond) {
          errorMessages.push(
            `${rulesInfo.label} must be between ${rulesInfo.range[0]} and ${rulesInfo.range[1]}.`
          );
        }
      }
      if (isGte) {
        const cond = value < rulesInfo.gte;
        if (cond) {
          errorMessages.push(
            `${rulesInfo.label} must be greater than or equal to ${rulesInfo.gte}.`
          );
        }
      }
    });

    const extraCond = currentAge < calcInput;
    if (!extraCond) {
      errorMessages.push(`Payout Age must be greater than Current Age.`);
    }

    // result = (
    //   currentAgeCond &&
    //   avgReturnCond &&
    //   calcInputCond &&
    //   fundingAmntCond &&
    //   extraCond
    // );
    const hasErrors = errorMessages.length > 0;

    if (hasErrors && notification) {
      errorMessages = ['Calculator validation failed.', ...errorMessages];

      toast(errorMessages.join('\n'), { duration: 8000 });
    }

    // console.log('errorMessages', errorMessages);
    // console.log('hasErrors', hasErrors);
    // console.log('validateSearch state', state);
    //
    // console.log('currentAgeCond', currentAgeCond);
    // console.log('avgReturnCond', avgReturnCond);
    // console.log('calcInputCond', calcInputCond);
    // console.log('fundingAmntCond', fundingAmntCond);
    // console.log('extraCond', extraCond);
    // console.log('validateSearch result', result);
    return !hasErrors;
  }

  // handleSearch1(onlyUserProspect: boolean): any {
  //   return () => {
  //     this.handleSearch(onlyUserProspect);
  //   }
  // }

  async handleSearch(onlyUserProspect = false) {
    // this.searchCallbacks.forEach(callback => callback.cancel());
    // this.searchCallbacks = [];
    // const previous = this.searchCallbacks.shift();
    // if (previous) {
    //   previous.cancel();
    // }

    if (debug) console.log('onlyUserProspect', onlyUserProspect);
    const { state } = this;
    const {
      gender,
      currentAge,
      avgReturn,
      monthlyInstallment,
      retirementAge,
      calcInput: tempCalcInput,
      fundingAmnt,
    } = state as IState;

    const calcInput = Number(tempCalcInput);

    const baseQueryParams: { [key: string]: string } = {
      gender,
      current_age: currentAge.toString(),
      average_return: avgReturn.toString(),
      monthly_installment: monthlyInstallment.toString(),
      retirement_age: retirementAge.toString(),
      // payout_age: calcInput.toString(),
      funding_amount: fundingAmnt.toString(),
    };

    if (onlyUserProspect) {
      const userProspect = await this.getProspectCalculation({
        ...baseQueryParams,
        payout_age: calcInput.toString(),
      });

      this.setState({ userProspect, loading: false });
    } else {
      let payoutAges: number[] = [80, 85, 90];
      if (!payoutAges.includes(calcInput)) {
        payoutAges = [...payoutAges, calcInput];
      }

      const [data80, data85, data90, userProspectTemp]: IProspect[] =
        await Promise.all(
          payoutAges.map((payout_age: number) => {
            return this.getProspectCalculation({
              ...baseQueryParams,
              payout_age: payout_age.toString(),
            });
          })
        );

      let userProspect;
      // console.log('userProspectTemp', userProspectTemp);
      if (!userProspectTemp) {
        if (calcInput === 80) {
          userProspect = data80;
        } else if (calcInput === 85) {
          userProspect = data85;
        } else if (calcInput === 90) {
          userProspect = data90;
        }
      } else {
        userProspect = userProspectTemp;
      }

      this.setState({
        baseProspects: [data80, data85, data90],
        maxWithSavvly: data90?.with_savvly,
        maxWithOutSavvly: data90?.without_savvly,
        userProspect,
        loading: false,
      });
    }
  }

  onClickChartDimension(dimension: Dimension): (event: any) => void {
    return () => {
      // console.log('dimension', dimension);
      // console.log('event', event);
      this.setState({
        chartDimension: dimension !== 'vertical' ? 'horizontal' : 'vertical',
      });
    };
  }

  // 'horizontal-bars'
  // 'vertical-bars'
  getChartBtnClassName(name: string): string {
    const { state } = this;
    const { chartDimension } = state as IState;
    let result = '';
    result = `${name}-bars`;
    if (chartDimension === name) {
      result += ' active';
    }
    return result;
  }

  getCalculateContainerClassName(): string {
    const { state } = this;
    const { chartDimension } = state as IState;
    const additional = chartDimension === 'vertical' ? ' vr-look' : '';
    return `container js-vertical${additional}`;
  }

  formatAmount(value: number | string): string {
    return numeral(value).format('$0,0');
  }

  // formatAmountForYearsOld(value: number | string): string {
  //   const newValue = value.toString().concat('yo');
  //   console.log(typeof value);
  //   return numeral(newValue).format('0,0y');
  // }

  calculateWidthForBars(value: number) {
    const { state } = this;
    const { maxWithSavvly } = state as IState;

    const calcPercentage = value / maxWithSavvly;

    const totalPixels = withSavvlyMaxWidth * calcPercentage;

    return totalPixels;
  }

  render() {
    if (debug) console.log('render this', this);

    const state = this.state as IState;

    const { fundingAmntShow } = state;

    const formatAmountValue: string = fundingAmntShow
      ? this.formatAmount(state.fundingAmntShow)
      : '';

    // const formatValueForYo: string = calcInput
    //   ? this.formatAmountForYearsOld(state.calcInput)
    //   : '';

    // this.setState({...this.state, isLoggedIn: true});

    if (!state.isLoggedIn)
      return (
        <div className='loginContainer'>
          <h1>Enter Password</h1>
          <input
            type="password"
            className='password-input'
            onChange={ e => this.setState({password: e.target.value}) }
            value={state.password}
          />
          <button className="loginbtn" onClick={ () => {
            if (state.password === "Napa2022!")
              this.setState({isLoggedIn: true});
            else
              alert("BAD CREDENTIALS");

          }}>ACCESS</button>
        </div>
      )

    return (
      <BlockUi
        blocking={state.loading}
        loader={<span className="loader"></span>}
      >
        <Toaster position="top-right" />
        <div className="login no-header">
          <div className="divider">
            <div className="site">
              <section className="calculate-container">
                <div>
                  <div className="calculate grid_flex lg-flex-column">
                    <div className="calculate-sidebar">
                      <div className="container">
                        <div className="title-content"></div>

                        <div className="display-options grid_flex ai-center jc-between">
                          <div>
                            <button
                              type="button"
                              className={this.getChartBtnClassName(
                                'horizontal'
                              )}
                              onClick={this.onClickChartDimension('horizontal')}
                            >
                              <svg
                                width="33"
                                height="33"
                                viewBox="0 0 33 33"
                                fill="none"
                                xmlns="http://www.w3.org/2000/svg"
                              >
                                <rect
                                  x="33"
                                  width="33"
                                  height="33"
                                  rx="6"
                                  transform="rotate(90 33 0)"
                                  fill="#176A78"
                                />
                                <rect
                                  x="6"
                                  y="9.71436"
                                  width="2.71429"
                                  height="19"
                                  rx="1.35714"
                                  transform="rotate(-90 6 9.71436)"
                                  fill="white"
                                  fillOpacity="0.8"
                                />
                                <rect
                                  x="6"
                                  y="15.1428"
                                  width="2.71429"
                                  height="9.22857"
                                  rx="1.35714"
                                  transform="rotate(-90 6 15.1428)"
                                  fill="white"
                                  fillOpacity="0.8"
                                />
                                <rect
                                  x="6"
                                  y="20.5715"
                                  width="2.71428"
                                  height="16.2857"
                                  rx="1.35714"
                                  transform="rotate(-90 6 20.5715)"
                                  fill="white"
                                  fillOpacity="0.8"
                                />
                                <rect
                                  x="6"
                                  y="26"
                                  width="2.71428"
                                  height="13.0286"
                                  rx="1.35714"
                                  transform="rotate(-90 6 26)"
                                  fill="white"
                                  fillOpacity="0.8"
                                />
                              </svg>
                            </button>
                            <button
                              type="button"
                              className={this.getChartBtnClassName('vertical')}
                              onClick={this.onClickChartDimension('vertical')}
                            >
                              <svg
                                width="33"
                                height="33"
                                viewBox="0 0 33 33"
                                fill="none"
                                xmlns="http://www.w3.org/2000/svg"
                              >
                                <rect
                                  x="0.5"
                                  y="0.5"
                                  width="32"
                                  height="32"
                                  rx="5.5"
                                  fill="#176A78"
                                  stroke="#55C4CB"
                                />
                                <rect
                                  x="9.71436"
                                  y="27"
                                  width="2.71429"
                                  height="19"
                                  rx="1.35714"
                                  transform="rotate(180 9.71436 27)"
                                  fill="white"
                                  fillOpacity="0.8"
                                />
                                <rect
                                  x="15.1431"
                                  y="27"
                                  width="2.71429"
                                  height="9.22857"
                                  rx="1.35714"
                                  transform="rotate(180 15.1431 27)"
                                  fill="white"
                                  fillOpacity="0.8"
                                />
                                <rect
                                  x="20.5713"
                                  y="27"
                                  width="2.71428"
                                  height="16.2857"
                                  rx="1.35714"
                                  transform="rotate(180 20.5713 27)"
                                  fill="white"
                                  fillOpacity="0.8"
                                />
                                <rect
                                  x="26"
                                  y="27"
                                  width="2.71428"
                                  height="13.0286"
                                  rx="1.35714"
                                  transform="rotate(180 26 27)"
                                  fill="white"
                                  fillOpacity="0.8"
                                />
                              </svg>
                            </button>
                          </div>

                          <div className="grid_flex fd-column custom-switch-container">
                            <div className="grid_flex">
                              <p className="gender-option-1">Male</p>
                              <label className="switch margin-right">
                                <input
                                  type="checkbox"
                                  id="gender"
                                  name="gender"
                                  onChange={this.handleChange(
                                    'gender',
                                    state.gender
                                  )}
                                  value={state.gender}
                                />
                                <span className="slider round"></span>
                              </label>
                              <p className="gender-option-2">Female</p>
                            </div>
                          </div>
                        </div>

                        <div className="options-content grid_flex ai-base jc-between">
                          <div className="current-age">
                            {/* for="current-age" */}
                            <label>Current Age</label>
                            <input
                              type="number"
                              name="current-age"
                              id="current-age"
                              onChange={this.handleChange('currentAge')}
                              value={state.currentAge}
                            />
                          </div>

                          <div className="avg-return">
                            {/* for="return" */}
                            <label>
                              <span className="avg-return-title--info ai-center">
                                Avg. Return
                                <span className="info" title="informations">
                                  <svg
                                    width="20"
                                    height="21"
                                    viewBox="0 0 20 21"
                                    fill="none"
                                    xmlns="http://www.w3.org/2000/svg"
                                  >
                                    <circle
                                      cx="9.61539"
                                      cy="9.61539"
                                      r="9.11539"
                                      stroke="#CCCCCC"
                                    />
                                    <path
                                      d="M10.4164 7.51936V13.6154H8.42438V7.51936H10.4164ZM10.4164 5.07136V6.64336H8.42438V5.07136H10.4164Z"
                                      fill="#CCCCCC"
                                    />
                                  </svg>
                                </span>
                              </span>
                              <span className="avg-return-input-wrapper">
                                <input
                                  type="number"
                                  id="return"
                                  name="return"
                                  onChange={this.handleChange('avgReturn')}
                                  value={state.avgReturn}
                                  pattern="\d*"
                                  maxLength={2}
                                />
                                <span className="percentage">%</span>
                                <span className="increase-arrow">
                                  <svg
                                    width="19"
                                    height="10"
                                    viewBox="0 0 19 10"
                                    fill="none"
                                    xmlns="http://www.w3.org/2000/svg"
                                  >
                                    <path
                                      d="M18.0835 10L0.91671 10C0.104351 10 -0.309492 9.05771 0.272954 8.49823L8.85637 0.253241C9.20891 -0.0853923 9.79135 -0.0853922 10.1439 0.253241L18.7273 8.49824C19.3097 9.05772 18.8959 10 18.0835 10Z"
                                      fill="white"
                                    />
                                  </svg>
                                </span>
                                <span className="decrease-arrow">
                                  <svg
                                    width="19"
                                    height="10"
                                    viewBox="0 0 19 10"
                                    fill="none"
                                    xmlns="http://www.w3.org/2000/svg"
                                  >
                                    <path
                                      d="M0.916458 0H18.0833C18.8956 0 19.3095 0.942285 18.727 1.50177L10.1436 9.74676C9.7911 10.0854 9.20865 10.0854 8.85612 9.74676L0.272703 1.50177C-0.309744 0.942285 0.104099 0 0.916458 0Z"
                                      fill="white"
                                    />
                                  </svg>
                                </span>
                              </span>
                            </label>
                          </div>
                        </div>
                      </div>
                    </div>

                    <div className="calculate-main">
                      <div className={this.getCalculateContainerClassName()}>
                        <div className="calculate-statistics-container">
                          <div className="calculate-main-header">
                            <div className="fundings-wrapper">
                              <p className="amount-title">Funding amount</p>
                              <div className="grid_flex ai-center  md-flex-wrap md-flex-between">
                                <p
                                  className={`amount-option ${
                                    state.fundingAmnt === 100000 ? 'active' : ''
                                  }`}
                                  onClick={this.handleChange(
                                    'fundingAmntOptions',
                                    100000
                                  )}
                                >
                                  $100,000
                                </p>
                                <p
                                  className={`amount-option ${
                                    state.fundingAmnt === 150000 ? 'active' : ''
                                  }`}
                                  onClick={this.handleChange(
                                    'fundingAmntOptions',
                                    150000
                                  )}
                                >
                                  $150,000
                                </p>
                                <p
                                  className={`amount-option ${
                                    state.fundingAmnt === 200000 ? 'active' : ''
                                  }`}
                                  onClick={this.handleChange(
                                    'fundingAmntOptions',
                                    200000
                                  )}
                                >
                                  $200,000
                                </p>

                                <input
                                  type="text"
                                  name="custom-amount"
                                  id="custom-amount"
                                  // placeholder="$175,000"
                                  className="amount-option amount-option-last"
                                  onChange={this.handleChange('fundingAmnt')}
                                  value={formatAmountValue}
                                />
                                {/* for="custom-amount" */}
                                <label className="screen-reader-text">
                                  Custom Amount
                                </label>
                              </div>
                            </div>
                          </div>

                          <div className="calculate-main-body">
                            <p className="payout-title">Payout Age</p>
                            <div className="calculate-main-compare">
                              {state.baseProspects.map((ageless, index) => {
                                const sizeMappings: { [key: string]: string } =
                                  {
                                    '0': 'small',
                                    '1': 'medium',
                                    '2': 'large',
                                  };

                                const widthPixelsWithoutSavvly =
                                  this.calculateWidthForBars(
                                    ageless.without_savvly
                                  );
                                const widthPixelsWithSavvly =
                                  this.calculateWidthForBars(
                                    ageless.with_savvly
                                  );
                                const size = sizeMappings[index];
                                return (
                                  <div
                                    key={index}
                                    className="grid_flex ai-center"
                                  >
                                    <div className="compare-option">
                                      <p>
                                        {ageless?.payout_age}
                                        <span> yo</span>
                                      </p>
                                    </div>
                                    <div className="compare-bars">
                                      <div className="grid_flex ai-center">
                                        <span
                                          style={{
                                            transition: 'width 2s',
                                            width:
                                              size === 'large'
                                                ? '406px'
                                                : `${widthPixelsWithSavvly}px`,
                                          }}
                                          className={`compare-bar-savvly compare-bar-savvly-large`}
                                        ></span>
                                        <p className="compare-amount">
                                          {this.formatAmount(
                                            ageless.with_savvly
                                          )}
                                        </p>
                                        <p className="compare-description">
                                          Savvly
                                        </p>
                                      </div>
                                      <div className="grid_flex ai-center">
                                        <span
                                          style={{
                                            width: `${widthPixelsWithoutSavvly}px`,
                                          }}
                                          className={`compare-bar-noSavvly compare-bar-noSavvly-large`}
                                        ></span>
                                        <p className="compare-amount">
                                          {this.formatAmount(
                                            ageless.without_savvly
                                          )}
                                        </p>
                                        <p className="compare-description">
                                          Without Savvly
                                        </p>
                                      </div>
                                    </div>
                                  </div>
                                );
                              })}
                              <div className="grid_flex ai-center custom-funding-amount-y">
                                <div className="compare-option">
                                  <input
                                    className="calculate-input"
                                    type="text"
                                    name="compare-disc"
                                    id="compare-disc"
                                    onChange={this.handleChange('calcInput')}
                                    value={state.calcInput}
                                  />
                                  <span
                                    className="text-for-calc-input"
                                    style={{
                                      position: 'relative',
                                      display: 'inline-block',
                                      fontSize: '14px',
                                      // marginLeft: '-17px',
                                      // marginTop: '6.5px',
                                      top: '0px',
                                      right: '16.5px',
                                      color: '#333333',
                                    }}
                                  >
                                    yo
                                  </span>
                                </div>
                                <div className="compare-bars">
                                  <div className="grid_flex ai-center">
                                    <span
                                      style={{
                                        width: `${this.calculateWidthForBars(
                                          state.userProspect.with_savvly
                                        )}px`,
                                      }}
                                      className={`compare-bar-savvly compare-bar-savvly-large`}
                                    ></span>
                                    <p className="compare-amount">
                                      {`${this.formatAmount(
                                        state.userProspect.with_savvly
                                      )}`}
                                    </p>
                                    <p className="compare-description">
                                      Savvly
                                    </p>
                                  </div>
                                  <div className="grid_flex ai-center">
                                    <span
                                      style={{
                                        width: `${this.calculateWidthForBars(
                                          state.userProspect.without_savvly
                                        )}px`,
                                      }}
                                      className={`compare-bar-noSavvly compare-bar-noSavvly-large`}
                                    ></span>
                                    <p className="compare-amount">
                                      {`${this.formatAmount(
                                        state.userProspect.without_savvly
                                      )}`}
                                    </p>
                                    <p className="compare-description">
                                      Without Savvly
                                    </p>
                                  </div>
                                </div>
                              </div>
                            </div>
                          </div>
                        </div>

                        <div className="calculate-main-footer">
                          <button
                            className="button-normal button-wide btn-white-bg margin-top"
                            type="button"
                            disabled={true}
                            style={{ display: `none` }}
                          >
                            Share
                            <span className="arrow-right">
                              <svg
                                width="10"
                                height="15"
                                viewBox="0 0 10 15"
                                fill="none"
                                xmlns="http://www.w3.org/2000/svg"
                              >
                                <path
                                  d="M1.08533 0.000252474C0.523498 -0.0121479 0.0575308 0.433788 0.0456074 0.99562C0.0389303 1.30706 0.175334 1.60467 0.415711 1.80307L6.64165 7.13666L0.415234 12.4683C-0.0378565 12.8012 -0.135152 13.438 0.19775 13.891C0.530652 14.3441 1.16736 14.4414 1.62045 14.1085C1.66195 14.078 1.70058 14.0446 1.73683 14.0084L8.86513 7.90977C9.29246 7.54492 9.34349 6.90296 8.97864 6.47515C8.94382 6.43461 8.90614 6.39645 8.86513 6.36164L1.73683 0.256845C1.55702 0.0970707 1.32571 0.00597572 1.08533 0.000252474Z"
                                  fill="white"
                                />
                              </svg>
                            </span>
                          </button>
                          <p className="disclaimer">
                            For illustration purposes only. This page is not
                            investment or financial advice. Forfeiture gains are
                            based on recent actuarial tables and withdrawal
                            scenarios. Past performance is not indicative of
                            future results. Consult your financial advisors to
                            consider your unique financial situation prior to
                            investing.
                          </p>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </section>

              {/* <div className="container darker-bg height-fix">

                      <div id="site_search" className="site-search">
                          <label for="searchTerm" className="screen-reader-text">Search</label>
                          <input type="search" id="searchTerm" placeholder="Search for client or prospect" />
                          <button type="button" id="searchButton" className="search-button">
                              <span>
                                  <svg width="21" height="21" viewBox="0 0 21 21" fill="none" xmlns="http://www.w3.org/2000/svg">
                                      <path d="M8.60034 17.2145C10.371 17.2145 12.0067 16.6744 13.3727 15.7631L18.3137 20.708C18.7015 21.0962 19.3423 21.0962 19.747 20.708L20.7083 19.746C21.0961 19.3579 21.0961 18.7165 20.7083 18.3115L15.7504 13.3834C16.661 12.0164 17.2007 10.3793 17.2007 8.60725C17.2007 3.86482 13.339 0 8.60034 0C3.86172 0 0 3.86482 0 8.60725C0 13.3497 3.84486 17.2145 8.60034 17.2145ZM8.60034 3.37539C11.484 3.37539 13.828 5.72129 13.828 8.60725C13.828 11.4932 11.484 13.8391 8.60034 13.8391C5.71669 13.8391 3.37268 11.4932 3.37268 8.60725C3.37268 5.72129 5.71669 3.37539 8.60034 3.37539Z" fill="black"/>
                                  </svg>
                              </span>
                          </button>
                      </div>

                      <div className="hr-line"></div>

                      <div className="overall-container margin-top-double">
                          <div className="grid_flex">
                              <div className="grid-col-6">
                                  <h3>Overall Balance</h3>
                                  <div className="overall-box"></div>
                              </div>
                              <div className="grid-col-6">
                                  <h3>Balances by client</h3>
                                  <div className="overall-box"></div>
                              </div>
                          </div>
                      </div>
                  </div> */}
            </div>
          </div>
        </div>
      </BlockUi>
    );
  }
}
/// /////////////////////////////////////////////////////////////////////////////
