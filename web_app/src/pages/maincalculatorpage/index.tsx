// @ts-ignore
import { MainCalculatorTemplate } from '@/templates/MainCalculatorTemplate';
import { useRouter } from 'next/router';
import Calculator from '../../components/Calculator';

const Index = () => {
  // @ts-ignore
  const router = useRouter();

  return (
    <MainCalculatorTemplate>
      <Calculator></Calculator>
    </MainCalculatorTemplate>
  );
};

export default Index;
