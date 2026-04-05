/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_memcmp.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: tsellak <tsellak@student.1337.ma>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/18 22:59:54 by tsellak           #+#    #+#             */
/*   Updated: 2025/10/29 02:39:22 by tsellak          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

int	ft_memcmp(const void *s1, const void *s2, size_t n)
{
	const unsigned char	*c_s1;
	const unsigned char	*c_s2;

	c_s1 = (const unsigned char *)s1;
	c_s2 = (const unsigned char *)s2;
	while (n && (*c_s1 == *c_s2))
	{
		n--;
		c_s1++;
		c_s2++;
	}
	if (n == 0)
		return (0);
	return (*c_s1 - *c_s2);
}
