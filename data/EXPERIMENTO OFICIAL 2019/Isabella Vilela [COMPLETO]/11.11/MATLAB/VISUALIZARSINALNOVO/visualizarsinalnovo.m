Fs=512;
m=2560;

isabellavilelaagua10= load ('isabellavilelaagua10_data.txt'); %acucar1

Ts=1/Fs;
t_final=(m-1)*Ts;
t=0:Ts:t_final;

c3=isabellavilelaagua10(1:m,2);
c4=isabellavilelaagua10(1:m,3);
c3c4=(c3-c4);
smin=min(c3c4);
smax=max(c3c4);
sinal=(c3c4-smin*ones(size(c3c4)))/(smax-smin);

save isabellavilelaagua10_data.txt sinal -ascii

% figure(1);plot(t,c3);
% figure(2);plot(t,c4);
% figure(3);plot(t,c3);hold on;plot(t,c4,'c');
% figure(4);plot(t,sinal);

f=-Fs/2:Fs/(m-1):Fs/2;
S=fftshift(fft(sinal,[]));
figure(5);plot(f,abs(S))
%corrigir para exibir de 0 até Fs/2

% figure(6);pwelch(sinal,[],[],[],Fs); % Calculo usando a Fs

figure(7);
% subplot(2,2,1);plot(t,c3);hold on;plot(t,c4,'c');
subplot(2,2,1);plot(t,c3c4)
subplot(2,2,2);plot(t,sinal);
subplot(2,2,3);plot(f,abs(S));
subplot(2,2,4);pwelch(sinal,[],[],[],Fs);
savefig('isabellavilelaagua10_data.fig');

 
