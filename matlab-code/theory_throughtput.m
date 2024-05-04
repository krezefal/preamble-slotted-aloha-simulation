clc;
close all;

%% CONSTS
% SIM CONSTANTS

CH_NUM = 6:10;

DTP_LEN = 1;
MIN_EP_LEN = 0;
MAX_EP_LEN = 1;
EP_LEN_STEP = 0.1;
% SLOTS_LEN is EP_LEN with DTP_LEN
SLOTS_LEN = DTP_LEN+MIN_EP_LEN:EP_LEN_STEP:DTP_LEN+MAX_EP_LEN;

MAX_LAMBD = 2;
LAMBD_STEP = 0.01;
LAMBDAS = 0:LAMBD_STEP:MAX_LAMBD;

% MATH CONSTANTS
INFINITY = 10;

% PROG CONSTANTS
ROUNDING = '%.4f';
SAVE_PATH = strcat('../graphs/matlab');


%% CALCULATING T(λ)  

for i = 1:length(CH_NUM)
    ch_num = CH_NUM(i);
    fprintf('КОЛ-ВО КАНАЛОВ = %d:\n', ch_num);

    max_throughputs = zeros(1, length(SLOTS_LEN));
    optimal_lambdas = zeros(1, length(SLOTS_LEN));

    figure;
    hold on;
    for j = 1:length(SLOTS_LEN)
        slot_len = SLOTS_LEN(j);
        format_str = sprintf(['Итерация расчета #%d: длина окна ' ...
            '= %s (ФИ=%s, ФП=%s)\n'], j, ROUNDING, ROUNDING, ROUNDING);
        fprintf(format_str, slot_len, slot_len-DTP_LEN, DTP_LEN);

        throughputs = zeros(1, length(LAMBDAS));
        for k = 1:length(LAMBDAS)
            lambda = LAMBDAS(k);
            if lambda == 0
                lambda = 0.0001;
            end
            % format_str = sprintf('======( λ = %s )======\n', ROUNDING);
            % fprintf(format_str, lambda);

            throughputs(k) = calc_throughput(lambda, slot_len, ch_num, ...
                INFINITY);
        end

        plot(LAMBDAS, throughputs, 'DisplayName', ['Длина окна = ', ...
            num2str(slot_len)]);
        
        [max_throughput, index] = find_max_throughput(throughputs);
        max_throughputs(j) = max_throughput;
        optimal_lambdas(j) = LAMBDAS(index);
    end

    fprintf('\n')
    for j = 1:length(max_throughputs)
        format_str = sprintf(['Макс. T(λ) на итерации #%d = %s ' ...
            '(λ = %s)\n'], j, ROUNDING, ROUNDING);
        fprintf(format_str, max_throughputs(j), optimal_lambdas(j));
    end
    fprintf('\n')

    hold off;
    legend('Location', 'southeast');
    xlabel('Интенсивность вх. потока');
    ylabel('T(λ)');
    xlim('auto')
    ylim('auto')
    title_str = sprintf(['Зависимость пропускной способности от ' ...
        'интенсивности вх. потока\n(аналитический расчет, кол-во ' ...
        'каналов %d)'], ch_num);
    title(title_str);
    filename = sprintf('/%dch_lambd_step_%.4f_throughput_theory', ...
        ch_num, LAMBD_STEP);
    savefig([SAVE_PATH, filename, '.fig']);
    saveas(gcf, [SAVE_PATH, filename, '.png']);
end

function throughput = calc_throughput(lambda, slot_len, ch_num, INFINITY)
    term1 = slot_len * lambda * exp(-slot_len * lambda);
    
    term2 = 0.0;
    for l = 1:ch_num
        multiplier1 = nchoosek(ch_num-1, l-1) * ...
            (slot_len * lambda)^(ch_num-l) * ...
            exp(-slot_len * lambda * ch_num);
        
        multiplier2 = calc_multiplier2(l, lambda, slot_len, INFINITY);
        term2 = term2 + multiplier1 * multiplier2;
    end
    
    throughput = (term1 + term2) / slot_len;
end

function multiplier2 = calc_multiplier2(l, lambd, slot_len, INFINITY)
    multiplier2 = 0.0;
    users_in_channels_comb = generate_users_in_channels(INFINITY, l);
    [~, num_combs] = size(users_in_channels_comb);
    for i = 1:num_combs
        users_in_channels = users_in_channels_comb{i};
        if sum(users_in_channels) == 0 || any(users_in_channels == 1)
            continue;
        end
        
        usr_sum = sum(users_in_channels);
        
        if usr_sum <= l
            tmp = (usr_sum / l) * (1 - 1/l)^(usr_sum - 1);
        else
            tmp = (1 - 1/usr_sum)^(usr_sum - 1);
        end
        
        tmp1 = power(slot_len * lambd, usr_sum);
        tmp2 = prod(factorial(users_in_channels));
        tmp = tmp * (tmp1 / tmp2);
        
        multiplier2 = multiplier2 + tmp;
    end
end

function users_in_channels_comb = generate_users_in_channels(m, l)
    function result = generate_combinations_helper(curr_combination, depth)
        if depth == l
            result = {curr_combination};
            return;
        end
        
        result = {};
        for num = 0:m
            new_combination = [curr_combination, num];
            result = [result, ...
                generate_combinations_helper(new_combination, depth + 1)];
        end
    end

    initial_combination = [];
    users_in_channels_comb = ...
        generate_combinations_helper(initial_combination, 0);
end

function [max_throughput, index] = find_max_throughput(throughputs)
    max_throughput = 0.0;
    index = 1;
    for i = 1:length(throughputs)
        if throughputs(i) > max_throughput
            max_throughput = throughputs(i);
            index = i;
        end
    end
end
