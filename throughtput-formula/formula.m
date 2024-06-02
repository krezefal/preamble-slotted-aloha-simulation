global INFINITY;
INFINITY = 10;

disp(calc_throughput(1.775, 1, 1)); % 0.5482
disp(calc_throughput(0.836, 1.6, 4)); % 0.3739
disp(calc_throughput(0.62, 2, 6)); % 0.3016
disp(calc_throughput(1, 1, 10)); % 0.5972 - didn't check manually


function throughput = calc_throughput(lambda, slot_len, ch_num)
    term1 = slot_len * lambda * exp(-slot_len * lambda);
    
    term2 = 0.0;
    for l = 1:ch_num
        multiplier1 = nchoosek(ch_num-1, l-1) * ...
            (slot_len * lambda)^(ch_num-l) * ...
            exp(-slot_len * lambda * ch_num);
        
        multiplier2 = calc_multiplier2(l, lambda, slot_len);
        term2 = term2 + multiplier1 * multiplier2;
    end
    
    throughput = (term1 + term2) / slot_len;
end

function multiplier2 = calc_multiplier2(l, lambd, slot_len)
    multiplier2 = 0.0;
    global INFINITY;
    users_in_channels_comb = generate_users_in_channels(INFINITY, l);
    [~, num_combs] = size(users_in_channels_comb);
    for i = 1:num_combs
        users_in_channels = users_in_channels_comb{i};
        if sum(users_in_channels) == 0
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
    function result = gen_combs_recursion(curr_combination, depth)
        if depth == l
            result = {curr_combination};
            return;
        end
        
        result = {};
        for num = 0:m
            if  num == 1
                continue
            end
            new_combination = [curr_combination, num];
            result = [result, ...
                gen_combs_recursion(new_combination, depth + 1)];
        end
    end

    initial_combination = [];
    users_in_channels_comb = ...
        gen_combs_recursion(initial_combination, 0);
end
