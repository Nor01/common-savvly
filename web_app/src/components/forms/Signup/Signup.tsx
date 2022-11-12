import { NextRouter, withRouter } from 'next/router';
/* eslint-disable no-useless-escape */
import toast, { Toaster } from 'react-hot-toast';

import { Component } from 'react';
/* eslint-disable unused-imports/no-unused-vars */
import axios from 'axios';

import statesZipCodes from './statesZipcodes';

// import styles from './Signup.Module.scss';
// const axios = require('axios').default;
interface WithRouterProps {
  router: NextRouter;
}

// const x: WithRouterProps = {} as WithRouterProps

interface IState {
  userName: string | number | readonly string[] | undefined;
  firstName: string;
  lastName: string;
  address: string;
  addressDetails: string;
  city: string;
  usState: string;
  zipcode: string;
  finra: string;
  phone: string;
  email: string;
  companyFinra: string;
  companyName: string;
  // userName: string;
  password: string;
  confirmPassword: string;
  errors: string;
  isCompany: string;
}

const defaultState: Partial<IState> = {
  firstName: '',
  lastName: '',
  address: '',
  addressDetails: '',
  city: '',
  usState: '',
  zipcode: '',
  finra: '',
  phone: '',
  email: '',
  companyFinra: '',
  companyName: '',
  userName: '',
  password: '',
  confirmPassword: '',
};

// // DO NOT REMOVE !!, for testing purpose
// const defaultStateTesting: Partial<IState> = {
//   firstName: 'firstname test',
//   lastName: 'lastname test',
//   address: 'address 1',
//   addressDetails: 'address details ..',
//   city: 'city 1',
//   usState: 'NY',
//   zipcode: '00000',
//   finra: 'finra',
//   phone: '0000000000',
//   email: 'email@em.co',
//   companyFinra: 'company finra',
//   companyName: 'company name',
//   userName: 'testWERQWRTGEWTGH',
//   password: 'sEtb$51J#',
//   confirmPassword: 'sEtb$51J#',
// };
const statesList = [
  'NY',
  'PR',
  'VI',
  'MA',
  'RI',
  'NH',
  'ME',
  'VT',
  'CT',
  'NJ',
  'AE',
  'PA',
  'DE',
  'DC',
  'VA',
  'MD',
  'WV',
  'NC',
  'SC',
  'GA',
  'FL',
  'AA',
  'AL',
  'TN',
  'MS',
  'KY',
  'OH',
  'IN',
  'MI',
  'IA',
  'WI',
  'MN',
  'SD',
  'ND',
  'MT',
  'IL',
  'MO',
  'KS',
  'NE',
  'LA',
  'AR',
  'OK',
  'TX',
  'CO',
  'WY',
  'ID',
  'UT',
  'AZ',
  'NM',
  'NV',
  'CA',
  'AP',
  'HI',
  'AS',
  'GU',
  'PW',
  'FM',
  'MP',
  'MH',
  'OR',
  'WA',
  'AK',
];

export default withRouter(
  class Signup extends Component<WithRouterProps, any> {
    constructor(props: WithRouterProps) {
      super(props);

      // const x: MyComponentProps = {} as MyComponentProps
      // console.log('x', x)
      // const x: WithRouterProps = props;

      this.state = {
        // -----------------------------------------------------------------------
        ...defaultState,
        // -----------------------------------------------------------------------
        // DO NOT REMOVE !!, for testing purpose
        // ...defaultStateTesting,
        // -----------------------------------------------------------------------
        isCompany: 'individual',
        loading: false,
        errors: '',
      } as IState;

      this.submitForm = this.submitForm.bind(this);
      this.postRegisterAdvisor = this.postRegisterAdvisor.bind(this);
      this.redirection = this.redirection.bind(this);
    }

    // componentDidUpdate() {
    //   // const { state } = this.state as IState;
    //   if (this.state.errors.length > 0) {
    //     this.redirection();
    //   }
    // }
    // const baseUrl = 'https://simulator-dev-eastus.azurewebsites.net/register';

    // const baseUrl = 'http://localhost:5000/api/registration';
    // const baseUrl = 'https://savvly-py.azurewebsites.net/api/registration';  // removed by Danny
    baseUrl =
      'https://savvly-webapp-backend.azurewebsites.net/api/registration'; // Added by Danny

    postRegisterAdvisor(queryParams: any) {
      const {
        firstName,
        lastName,
        address,
        addressDetails,
        city,
        usState,
        zipcode,
        finra,
        phone,
        email,
        // companyFinra,
        // companyName,
        userName,
        password,
        isCompany,
      } = queryParams;

      const bodyPromise: object = {
        firstName,
        lastName,
        email,
        finra,
        phone,
        username: userName,
        password,
        isCompany: isCompany !== 'individual',
        address: {
          name: address,
          details: addressDetails,
          city,
          state: usState,
          zipCode: zipcode,
        },
        // company: {
        //   finra: companyFinra,
        //   name: companyName,
        // },
      };

      // const options = {
      //   // mode: 'no-cors',
      //   // headers: {
      //   //   'Content-Type': 'application/json',
      //   //   'Allow-Origin': '*',
      //   //   'Access-Control-Allow-Origin': '*',
      //   //   'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
      //   //   'Access-Control-Allow-Headers': 'Origin, Content-Type, X-Auth-Token',
      //   // },
      //   ...bodyPromise // JSON.stringify(bodyPromise),
      // };
      // function redirection() {
      //   //   return this.router.push({
      //   //     pathname: '/login',
      //   //     // query: { returnUrl: this.router.asPath }
      //   // });
      //   // return {
      //   //   redirect: {
      //   //     destination: '/maincalculatorpage',
      //   //     permanent: false,
      //   //   },
      //   // };
      // }
      // const baseUrl = 'https://simulator-dev-eastus.azurewebsites.net/register';

      // const baseUrl = 'http://localhost:5000/api/registration';
      const baseUrl = 'https://savvly-py.azurewebsites.net/api/registration';

      // const url = `${baseUrl}?${new URLSearchParams(queryParams)}`;

      return new Promise((resolve, reject) => {
        axios
          .post(baseUrl, bodyPromise)
          .then((response: any) => {
            if (response.status === 200) {
              if (response.data.isSuccess) {
                resolve(response.data);
                this.setState(defaultState);
                this.redirection();
                // setTimeout(() => { this.redirection(); }, 1000);
              } else {
                // redirection();

                reject(response.data);
              }
            } else {
              throw new Error('server error');
            }
          })
          .catch(reject);
      });
    }

    redirection(): void {
      this.props.router.push('/maincalculatorpage');
    }

    handleChange(name: any) {
      return (event: any) => {
        let nextPartialFormState: any = {};
        const { value } = event.target;
        if (name === 'isCompany') {
          nextPartialFormState = {
            isCompany: value === 'individual' ? 'company' : 'individual',
          };
        } else {
          nextPartialFormState = {
            [name]: value,
          };
        }

        this.setState(nextPartialFormState);
      };
    }

    paintInputErrors(keyString: any) {
      const { errors } = this.state as IState;
      return errors.includes(keyString);
    }

    validateRegister(nextPartialState: any, notification = true): boolean {
      // console.log('validateRegister this', this)
      // let result = true;
      const { state } = this;
      const nextState = { ...state, ...nextPartialState };

      const {
        // fullName,
        // address,
        // addressDetails,
        // city,
        usState,
        zipcode,
        // finra,
        phone,
        email,
        // companyFinra,
        // companyName,
        userName: _username,
        password,
        confirmPassword,
      } = nextState as IState;

      // interface IstatesZipCodes extends Object(statesZipCodes){};

      const userName: string = _username as string;
      const regex: RegExp =
        /^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,4})$/;

      const phoneRegex: RegExp =
        /^\s*(?:\+?(\d{1,3}))?[-. (]*(\d{3})[-. )]*(\d{3})[-. ]*(\d{4})(?: *x(\d+))?\s*$/;

      const passwordRegex: RegExp =
        /^(?=.*[0-9])(?=.*[!@#$%^&*])[a-zA-Z0-9!@#$%^&*]{6,16}$/;

      // const zipcodeRegex: RegExp = /(^[0-9]{2,}$)/;

      const usStateRegex: RegExp = /^[A-Z]{2}/;

      const usernameRegex: RegExp = /^[A-Za-z0-9]*$/;

      const rulesDict: { [key: string]: any } = {
        firstName: { length: 0, label: 'firstName', errorName: 'First Name' },
        userName: { length: 0, label: 'userName', errorName: 'User Name' },
        lastName: { length: 0, label: 'lastName', errorName: 'Last Name' },
        // address: { length: 0, label: 'address' },
        // addressDetails: { length: 0, label: 'addressDetails' },
        // city: { length: 0, label: 'city' },
        // usState: { length: 0, label: 'usState' },
        // zipcode: { length: 0, label: 'zipcode' },
        finra: { length: 0, label: 'finra', errorName: 'Finra' },
        phone: { length: 0, label: 'phone', errorName: 'Phone' },
        // companyFinra: { length: 0, label: 'companyFinra' },
        // companyName: { length: 0, label: 'companyName' },
        password: { length: 0, label: 'password', errorName: 'Password' },
        confirmPassword: {
          length: 0,
          label: 'confirmPassword',
          errorName: 'Confirm Password',
        },
      };

      let errorMessages: string[] = [];
      const errorsArray: string[] = [];
      const numberZipCode = Number(zipcode);
      const statesZipCodesListItem = statesZipCodes[usState] as number[];
      //  statesZipCodes[usState].includes(numberZipCode)
      //   doesItIncludeZipcode = Object.fromEntries(Object.entries(statesZipCodes: [string | unknown]).includes(numberZipCode: [string
      // | uknown]))

      if (!regex.test(email)) {
        errorMessages.push(`Email must be valid.`);
        errorsArray.push('email');
      }
      if (!phoneRegex.test(phone) && phone.length > 0) {
        if (phone.length > 15) {
          errorMessages.push(`Phone must not exceed 15 digits.`);
          errorsArray.push('phone');
        } else {
          errorMessages.push(`Phone must be valid.`);
          errorsArray.push('phone');
        }
      }
      if (!passwordRegex.test(password)) {
        errorMessages.push(
          `Password must be 6 to 16 characters long, contain at least one number and at least one of the following special characters !@#$%^&*.`
        );
        errorsArray.push('password');
      }
      if (
        zipcode.length > 0 &&
        !statesZipCodesListItem.includes(numberZipCode)
      ) {
        errorMessages.push(
          `Zip Code must contain 2 to 6 numbers and be valid with US State.`
        );
        errorsArray.push('zipcode');
      }
      if (!usStateRegex.test(usState) && usState.length > 0) {
        errorMessages.push(
          `State must contain 2 Capital Letters and be valid.`
        );
        errorsArray.push('usState');
      }
      if (!usernameRegex.test(userName)) {
        errorMessages.push(`Username must contain only letters and numbers.`);
        errorsArray.push('userName');
      }
      if (password !== confirmPassword) {
        errorMessages.push(`Password must be the same on both fields.`);
        errorsArray.push('confirmPassword');
      }

      Object.keys(rulesDict).forEach((key: string) => {
        const value = nextState[key] || [];
        const rulesInfo = rulesDict[key];
        const condition = rulesInfo.length < value.length;
        if (!condition) {
          errorMessages.push(`${rulesInfo.errorName} must not me empty.`);
          errorsArray.push(`${rulesInfo.label}`);
        }
      });

      const hasErrors = errorMessages.length > 0;

      if (hasErrors && notification) {
        errorMessages = ['Registration failed.', ...errorMessages];
        this.setState({ errors: errorsArray });
        toast(errorMessages.join('\n'), { duration: 8000 });
        // this.paintInputErrors(errorsArray);
      } else {
        // toast.success('Successfully sent for Registration!');
        this.setState({ loading: true });
        const promise = this.postRegisterAdvisor(nextState);
        // .then((res) => {
        //   this.setState({ loading: false })
        //   if (!res.isSuccess) {
        //     throw res;
        //     return;
        //   }
        //   toast.success('Registration successfully completed!');
        // })
        // .catch(error => {
        //   this.setState({ loading: false })
        //   toast.error('Registration failed: ' + error.errors[0]);
        // });

        toast.promise(promise, {
          loading: 'Loading',
          success: 'Registration successfully completed!',
          error: (error) => {
            let suffix = '';
            if (
              'errors' in error &&
              Array.isArray(error.errors) &&
              error.errors.length > 0
            ) {
              // suffix = ` ${error.errors[0]}`;
              suffix = ' ';
              // eslint-disable-next-line no-return-assign
              error.errors.forEach((item: string) => (suffix += `\n ${item}`));
            }
            return `Registration failed!${suffix}`;
          },
        });
      }

      return !hasErrors;
    }

    submitForm(event: any) {
      event.preventDefault();

      this.validateRegister(this.state);
      return false;
    }

    render() {
      const state = this.state as IState;

      return (
        <div className="sign-up-form default-form">
          <Toaster position="top-right" />
          <form
            id="registration_form"
            className="js-registration-form"
            action=""
            data-step="step_1"
          >
            <div className="form-header fd-column">
              <h2>Register</h2>
              {/* <a href="#" className="default-link">
              Not your RIA
            </a> */}
            </div>
            <div className="group">
              <label htmlFor="firstName">First Name</label>
              <input
                style={{ minHeight: '55px' }}
                type="text"
                id="firstName"
                className={
                  this.paintInputErrors('firstName')
                    ? 'input-error-validation'
                    : ''
                }
                placeholder="i.e. John"
                onChange={this.handleChange('firstName')}
                value={state.firstName}
              />
            </div>
            <div className="group">
              <label htmlFor="lastName">Last Name</label>
              <input
                style={{ minHeight: '55px' }}
                type="text"
                id="lastName"
                className={
                  this.paintInputErrors('lastName')
                    ? 'input-error-validation'
                    : ''
                }
                placeholder="i.e. Smith"
                onChange={this.handleChange('lastName')}
                value={state.lastName}
              />
            </div>
            <div className="group">
              <label htmlFor="address">Address</label>
              <input
                style={{ minHeight: '55px' }}
                type="text"
                id="address"
                className={
                  this.paintInputErrors('address')
                    ? 'input-error-validation'
                    : ''
                }
                placeholder="i.e. 123 Main St."
                onChange={this.handleChange('address')}
                value={state.address}
              />
              <label
                htmlFor="address-description"
                className="screen-reader-text"
              >
                Address Description
              </label>
              <input
                style={{ minHeight: '55px' }}
                type="text"
                id="address-description"
                className={
                  this.paintInputErrors('addressDetails')
                    ? 'input-error-validation'
                    : ''
                }
                placeholder="i.e. Suite 200"
                onChange={this.handleChange('addressDetails')}
                value={state.addressDetails}
              />
            </div>
            <div className="group grid_flex">
              <span className="city">
                <label htmlFor="city">City</label>
                <input
                  style={{ minHeight: '55px' }}
                  type="text"
                  id="city"
                  className={
                    this.paintInputErrors('city')
                      ? 'input-error-validation'
                      : ''
                  }
                  name="city"
                  placeholder="i.e. Maintown"
                  onChange={this.handleChange('city')}
                  value={state.city}
                />
              </span>
              <span className="state">
                <label htmlFor="usState">state</label>
                <select
                  name="usState"
                  id="usState"
                  placeholder="State"
                  style={{ maxHeight: '55px' }}
                  className={
                    this.paintInputErrors('usState')
                      ? 'input-error-validation'
                      : ''
                  }
                  onChange={this.handleChange('usState')}
                  value={state.usState}
                >
                  {statesList.map((stateItem, index) => {
                    return (
                      <option key={index} value={stateItem}>
                        {stateItem}
                      </option>
                    );
                  })}
                </select>
              </span>
              {/* <span className="state">
                <label htmlFor="usState">state</label>
                <input
                  style={{ minHeight: '55px' }}
                  type="text"
                  id="usState"
                  className={
                    this.paintInputErrors('usState')
                      ? 'input-error-validation'
                      : ''
                  }
                  name="usState"
                  placeholder="i.e. NY"
                  onChange={this.handleChange('usState')}
                  value={state.usState}
                />
              </span> */}
              <span className="zipcode">
                <label htmlFor="zipcode">zipcode</label>
                <input
                  style={{ minHeight: '55px' }}
                  type="number"
                  id="zipcode"
                  className={
                    this.paintInputErrors('zipcode')
                      ? 'input-error-validation'
                      : ''
                  }
                  name="zipcode"
                  placeholder="i.e. 92831"
                  onChange={this.handleChange('zipcode')}
                  value={state.zipcode}
                />
              </span>
            </div>
            <div className="group">
              <label htmlFor="finra-number">Finra Number</label>
              <input
                style={{ minHeight: '55px' }}
                type="text"
                id="finra-number"
                className={
                  this.paintInputErrors('finra') ? 'input-error-validation' : ''
                }
                placeholder="i.e. T0017112"
                onChange={this.handleChange('finra')}
                value={state.finra}
              />
            </div>
            <div className="group">
              <div className="grid_flex fd-column custom-switch-container">
                <div className="grid_flex">
                  <p
                    className="gender-option-1"
                    style={{ marginRight: '16px' }}
                  >
                    Individual
                  </p>
                  <label className="switch margin-right">
                    <input
                      type="checkbox"
                      id="gender"
                      name="gender"
                      onChange={this.handleChange('isCompany')}
                      value={state.isCompany}
                    />
                    <span className="slider round"></span>
                  </label>
                  <p className="gender-option-2">Firm</p>
                </div>
              </div>
            </div>
            <div className="group">
              <label htmlFor="phone-number">Phone Number</label>
              <input
                style={{ minHeight: '55px' }}
                type="text"
                id="phone-number"
                className={
                  this.paintInputErrors('phone') ? 'input-error-validation' : ''
                }
                placeholder="18887766938"
                onChange={this.handleChange('phone')}
                value={state.phone}
              />
            </div>
            <div className="group">
              <label htmlFor="email">email</label>
              <input
                style={{ minHeight: '55px' }}
                type="email"
                id="email"
                className={
                  this.paintInputErrors('email') ? 'input-error-validation' : ''
                }
                placeholder="prospector@savvly.com"
                onChange={this.handleChange('email')}
                value={state.email}
              />
            </div>

            {/* <div className="group">
            <label htmlFor="company-name">Firm Name</label>
            <input
              style={{ minHeight: '55px' }}
              type="text"
              id="company-name"
              className={
                this.paintInputErrors('companyName')
                  ? 'input-error-validation'
                  : ''
              }
              placeholder="i.e. Savvly Advisors"
              onChange={this.handleChange('companyName')}
              value={state.companyName}
            />
          </div>
          <div className="group">
            <label htmlFor="company-finra-number">
              Firm Registration Number
            </label>
            <input
              style={{ minHeight: '55px' }}
              type="text"
              id="finra-number"
              className={
                this.paintInputErrors('companyFinra')
                  ? 'input-error-validation'
                  : ''
              }
              placeholder="i.e. T0017112"
              onChange={this.handleChange('companyFinra')}
              value={state.companyFinra}
            />
          </div> */}
            <div className="group">
              <label htmlFor="userName">Username</label>
              <input
                style={{ minHeight: '55px' }}
                type="text"
                id="userName"
                className={
                  this.paintInputErrors('userName')
                    ? 'input-error-validation'
                    : ''
                }
                placeholder="i.e. savvlyUser34"
                onChange={this.handleChange('userName')}
                value={state.userName}
              />
            </div>
            <div className="group">
              <label htmlFor="company-finra-number">Password</label>
              <input
                style={{ minHeight: '55px' }}
                type="password"
                id="password"
                className={
                  this.paintInputErrors('password')
                    ? 'input-error-validation'
                    : ''
                }
                placeholder="&#9679;&#9679;&#9679;&#9679;&#9679;&#9679;&#9679;&#9679;&#9679;&#9679;&#9679;&#9679;&#9679;&#9679;&#9679;"
                onChange={this.handleChange('password')}
                value={state.password}
              />
            </div>
            <div className="group">
              <label htmlFor="company-finra-number">Confirm Password</label>
              <input
                style={{ minHeight: '55px' }}
                type="password"
                id="password-confirmation"
                className={
                  this.paintInputErrors('confirmPassword')
                    ? 'input-error-validation'
                    : ''
                }
                placeholder="&#9679;&#9679;&#9679;&#9679;&#9679;&#9679;&#9679;&#9679;&#9679;&#9679;&#9679;&#9679;&#9679;&#9679;&#9679;"
                onChange={this.handleChange('confirmPassword')}
                value={state.confirmPassword}
              />
            </div>
            <div className="submit-form">
              <button
                className="button-normal btn-blue-bg"
                type="submit"
                onClick={this.submitForm}
              >
                Register
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
            </div>
          </form>
        </div>
      );
    }
  }
);
